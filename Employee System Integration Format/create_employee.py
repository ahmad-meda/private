from datetime import datetime
from proxies.employee_message_proxy import LeadMessageHistoryProxy
from proxies.proxy import EmployeeProxy
from proxies.employee_session_proxy import EmployeeSessionProxy
from Utils.fields_to_add import agent_states
from Utils.current_field import remove_used_fields_and_return_next, remove_fields_by_name_and_return_next
from Utils.agents import get_employee_details, extract_data, skipped_employee_details
from Utils.fuzzy_logic import find_best_match
from Utils.choices import EmployeeChoices
from Utils.enum import DraftType
from Utils.sanitization import sanitize_messages
from Utils.name_separation import separate_name
from Utils.explanations import Explanations
from Utils.null_fields import get_null_fields
from Utils.dummy_functions import send_whatsapp_message, clear_session

def create_employee(contact_number:str, user_message:str):

    print("Entered Create Employee")

    # Boolean to regulate optional and mandatory fields.
    skip_optional_logic = False
    LeadMessageHistoryProxy.save_message(contact_number, "user", user_message)

     # Get the Sales Agent ID from thedatabase using the contact number
    agent_id, agent_name = EmployeeProxy.get_hr_id_by_contact(contact_number=contact_number)
    draft_table_id, draft_id, draft_existed = EmployeeProxy.get_draft(agent_id, DraftType.EMPLOYEE.value)
    EmployeeProxy._add_created_by_to_employee_record(employee_record_id=draft_id, hr_id=agent_id)

    # Get all the null fields from the employee record
    main_fields, optional_personal_fields, optional_employment_fields, optional_location_fields = get_null_fields(draft_id)
    # Im storing all the fields that have default values when a record is created over here, if the user answers this fields or skips it, then its added to the redis session list. the fields in this list arent asked again.
    session_fields = EmployeeSessionProxy.get_list(contact_number=contact_number)
    print(f"Session Fields: {session_fields}")

    # if is_hr_reminders and hr_scope are are not in the session fields then add then in the optional personal fields
    if "is_hr" not in session_fields:
        optional_personal_fields.append("is_hr")
    if "hr_scope" not in session_fields:
        optional_personal_fields.append("hr_scope")
    if "reminders" not in session_fields:
        optional_personal_fields.append("reminders")

    # Get the HR Employee Record - The output is class Employee
    employee_record = EmployeeProxy.get_employee_record(contact_number=contact_number)
    print(f"Employee Name: {employee_record.name}")
    print(f"Employee Group: {employee_record.group_id}") 
    print(f"Employee Company: {employee_record.company_id}") 
    

    # Auto-assign company when user has no group, after adding the company remive it from the main_fields list, so that it wont be asked.
    if "company_name" in main_fields:
        if employee_record.group_id is None:
            EmployeeProxy.update_employee_company(employee_id=draft_id, company_id=employee_record.company_id)
            #add the hr scope to the session fields so that it wont be aske since the user has no group - only add to session field if its not already there
            if "hr_scope" not in session_fields:
                EmployeeSessionProxy.add_to_list(contact_number=contact_number, items=["hr_scope"])
            main_fields.remove("company_name")

    print(f"Main Fields: {main_fields}")
    print(f"Optional Personal Fields: {optional_personal_fields}")
    print(f"Optional Employment Fields: {optional_employment_fields}")
    print(f"Optional Location Fields: {optional_location_fields}")

    #  if current field is main_fields.
    current_phase, remaining = remove_fields_by_name_and_return_next(used_fields=session_fields,
                                          mandatory_fields=main_fields,
                                          optional_personal_fields=optional_personal_fields,
                                          optional_employment_fields=optional_employment_fields,
                                          optional_location_fields=optional_location_fields)

    # Error Dictionary and Explanations Dictionary. 
    # Explanations are passed to the LLM basides the fields so the LLM knows what each field means and so that it can explain to the user. 
    error_dict = {}
    explanations = {}  # Clear explanations at the start of each iteration




    # ------------------------ Main Logic STARTS Here --------------------------



    # Add the user message to the Redis session history - Refer to session service and proxy Files
    EmployeeSessionProxy.add_message(contact_number, {"role": "user", "content": user_message})


    # Get the previous messages of the conversation from the redis session history. 
    # We are using this because Postgres DB History isn't deleteable and may cause context confusion when a new conversation starts.
    extraction_messages = EmployeeSessionProxy.get_messages(contact_number)

    # Last 2 messages from session history are passed to the LLM Extraction Agent. 
    # Passing too many previous messages may cause the extraction of a single/multiple field/s to occur in multiple iterations.
    extracted_data = extract_data(messages=extraction_messages[-2:])
    print(f"Extracted Data: {extracted_data}")


    # This is Fuzzy Logic, best way to explain - if you have a type, fuzzy logic corrects it.
    # If there isnt a match at all based on the users input, it returns the user choice itself.
    # This is so it gets passed to service function where an error is raised and recorded in the error dictionary, which is then passed to the LLM to inform the user regarding the issue.
    if extracted_data.full_name or extracted_data.work_policy_name or extracted_data.office_location_name or extracted_data.department_name or extracted_data.reporting_manager_name or extracted_data.role or extracted_data.company_name or extracted_data.gender :
        extracted_data.work_policy_name = find_best_match(user_input=extracted_data.work_policy_name, choices=EmployeeChoices.get_work_policy_choices(), threshold=85)
        extracted_data.office_location_name = find_best_match(user_input=extracted_data.office_location_name, choices=EmployeeChoices.get_office_location_choices(group_id=employee_record.group_id, company_id=employee_record.company_id), threshold=90)
        extracted_data.department_name = find_best_match(user_input=extracted_data.department_name, choices=EmployeeChoices.get_departments_choices(), threshold=85)
        extracted_data.reporting_manager_name = find_best_match(user_input=extracted_data.reporting_manager_name, choices=EmployeeChoices.get_reporting_manager_choices(hr_company_id=employee_record.company_id, hr_group_id=employee_record.group_id), threshold=85)
        extracted_data.role = find_best_match(user_input=extracted_data.role, choices=EmployeeChoices.get_role_choices(), threshold=85)
        extracted_data.company_name = find_best_match(user_input=extracted_data.company_name, choices=EmployeeChoices.get_companies_choices(group_id=employee_record.group_id, company_id=employee_record.company_id), threshold=85)
        extracted_data.gender = find_best_match(user_input=extracted_data.gender, choices=EmployeeChoices.get_gender_choices(), threshold=85)

        # No Fuzzy logic here, just manually splitting name into first, middle and last, sometimes the llm can be a pain.
        extracted_data.first_name, extracted_data.middle_name, extracted_data.last_name = separate_name(extracted_data.full_name)
    
    # I'm only running the service function when a field value has been extracted, this is in place so that unecessary db calls can be avoided.
    print("If any data has been extracted from the user message",extracted_data.model_dump(exclude_none=True))
    # Only run db service function if something has been extracted from the user message
    if extracted_data.model_dump(exclude_none=True):
        print("in if loop after extraction")
        print(extracted_data.model_dump(exclude_none=True))
        result = EmployeeProxy._adding_new_employee(employee_db_id=draft_id, 
                                                full_name=extracted_data.full_name, 
                                                contact_number=extracted_data.contact_number,
                                                company_name=extracted_data.company_name, 
                                                role=extracted_data.role, 
                                                work_policy_name=extracted_data.work_policy_name, 
                                                office_location_name=extracted_data.office_location_name, 
                                                department_name=extracted_data.department_name, 
                                                reporting_manager_name=extracted_data.reporting_manager_name, 
                                                first_name=extracted_data.first_name, 
                                                middle_name=extracted_data.middle_name, 
                                                last_name=extracted_data.last_name, 
                                                emailId=extracted_data.emailId, 
                                                designation=extracted_data.designation, 
                                                dateOfJoining=extracted_data.dateOfJoining, 
                                                dateOfBirth=extracted_data.dateOfBirth, 
                                                gender=extracted_data.gender, 
                                                home_latitude=extracted_data.home_latitude, 
                                                home_longitude=extracted_data.home_longitude,
                                                allow_site_checkin=extracted_data.allow_site_checkin,
                                                restrict_to_allowed_locations=extracted_data.restrict_to_allowed_locations,
                                                reminders=extracted_data.reminders,
                                                is_hr=extracted_data.is_hr,
                                                hr_scope=extracted_data.hr_scope,
                                                hr_company_id=employee_record.company_id,
                                                hr_group_id=employee_record.group_id)
        
        # Add reminders, is_hr, hr_scope to the session fields if they are extracted
        if extracted_data.office_location_name == "manager_skip" or extracted_data.office_location_name == "home_coordinates":
            EmployeeSessionProxy.add_to_list(contact_number=contact_number, items=["office_location_name"])
        if extracted_data.reminders is not None:
            EmployeeSessionProxy.add_to_list(contact_number=contact_number, items=["reminders"])
        if extracted_data.is_hr is not None:
            EmployeeSessionProxy.add_to_list(contact_number=contact_number, items=["is_hr"])
        if extracted_data.hr_scope is not None:
            EmployeeSessionProxy.add_to_list(contact_number=contact_number, items=["hr_scope"])

        # This is to handle the case where the user has given a wrong office location name when asked for multiple location check-ins, and the service function has returned an error.
        if extracted_data.multiple_office_locations_to_check_in is not None:
            # Add fuzzy logic to each location name in the list and give the final list with corrected names.
            corrected_location_names = []
            for location_name in extracted_data.multiple_office_locations_to_check_in:
                location_name = find_best_match(user_input=location_name, choices=EmployeeChoices.get_office_location_choices(group_id=employee_record.group_id, company_id=employee_record.company_id), threshold=85)
                corrected_location_names.append(location_name)
            # Save the office locations to the employee and to add any errors to the error dictionary.  
            result = EmployeeProxy.save_employee_office_locations(employee_id=draft_id, office_location_names=corrected_location_names)
            error_dict = result['errors']
        
        # Validate the updating of the draft - If there is an error in updating a certain field, that field of the extracted data will be set to None
        error_dict = result['errors']
        print(f"Error Dict: {error_dict}")


     # If there are errors in any fields, set those fields to None
     # IMPORTANT : Removing this will significantly break add employee agent.
    for field_name in error_dict:
        if hasattr(extracted_data, field_name):
            setattr(extracted_data, field_name, None)
            

    # Get null fields again, There was a reason I put this, I forgot :), BBut its important, DO NOT REMOVE.
    main_fields, optional_personal_fields, optional_employment_fields, optional_location_fields = get_null_fields(draft_id)

    # if is_hr_reminders and hr_scope are are not in the session fields then add then in the optional personal fields
    if "is_hr" not in session_fields:
        optional_personal_fields.append("is_hr")
    if "hr_scope" not in session_fields:
        optional_personal_fields.append("hr_scope")
    if "reminders" not in session_fields:
        optional_personal_fields.append("reminders")

    session_fields = EmployeeSessionProxy.get_list(contact_number=contact_number)
    print(f"Session Fields: {session_fields}")

    # Im not using the output anywhere but I need to run this function
    phase, remaining = remove_fields_by_name_and_return_next(used_fields=session_fields,
                                          mandatory_fields=main_fields,
                                          optional_personal_fields=optional_personal_fields,
                                          optional_employment_fields=optional_employment_fields,
                                          optional_location_fields=optional_location_fields)


    current_field, remaining_fields = remove_used_fields_and_return_next(data_object=extracted_data,
                                                                            mandatory_fields=main_fields,
                                                                            optional_personal_fields=optional_personal_fields,
                                                                            optional_employment_fields=optional_employment_fields,
                                                                            optional_location_fields=optional_location_fields)

    if current_phase == current_field:
        skip_optional_logic = True

    # Only enter this if the current field is not a mandatory field
    if current_field != "mandatory_fields" and skip_optional_logic == True:
        print("currently in optional fields")
        print(f"Remaining Fields: {remaining_fields}")
        skipped_fields = skipped_employee_details(messages=extraction_messages[-2:], fields=remaining_fields)
        print(f"Skipped Fields: {skipped_fields.skipped_fields}")
        if skipped_fields.skipped_fields is None:
            skipped_fields.skipped_fields = []
        EmployeeSessionProxy.add_to_list(contact_number=contact_number, items=skipped_fields.skipped_fields)
        current_field, remaining_fields = remove_fields_by_name_and_return_next(used_fields=skipped_fields.skipped_fields,
                                                mandatory_fields=main_fields,
                                                optional_personal_fields=optional_personal_fields,
                                                optional_employment_fields=optional_employment_fields,
                                                optional_location_fields=optional_location_fields)
    
    # This was added to handle the case where the user has given a wrong office location name when asked for multiple location check-ins, and the service function has returned an error.
    if current_field is None and len(remaining_fields) == 0 and error_dict != {}:
        response = get_employee_details(messages=extraction_messages, fields=remaining_fields, error_dict=error_dict, explanations=explanations)
        EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
        LeadMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
        print(f"Assistant: {response.message_to_user}")
        return
        
    # If there are no fields left to add and there are no errors to report then end the add employee agent interaction.
    if current_field is None and len(remaining_fields) == 0 and error_dict == {}:
        print("Adding in main database")
        add_result = EmployeeProxy._add_employee_in_main_database(draft_id=draft_id)
        print(f"adding in main database: ", add_result)
        
        # Create leave balances for the newly created employee
        if "new_employee_id" in add_result:
            new_employee_id = add_result["new_employee_id"]
            print(f"Creating leave balances for employee ID: {new_employee_id}")
            leave_balance_result = EmployeeProxy.create_leave_balances_for_employee(employee_id=new_employee_id)
            print(f"Leave balance creation result: {leave_balance_result}")
        
        LeadMessageHistoryProxy.clear_message_history(contact_number)
        EmployeeSessionProxy.clear_list(contact_number=contact_number) # clear the redis message history after the employee has been successfully added

        #Get the new employee Record
        added_employee = EmployeeProxy.get_employee_draft_record_by_id(employee_id=draft_id)
        end_message = f"Employee {added_employee.name} has been successfully added to the database!"
        EmployeeProxy._delete_draft(draft_id=draft_table_id)
        send_whatsapp_message(contact_number, end_message)
        clear_session(contact_number)
        return
    
    # When the user first tries to add an employee, after the first message, we display all the fields and what they require to add an employee.
    # All the fields are listed and an example of what the field value should be is also given.
    # Additionally, certain fields explanations are passed as well to make sure the LLM doesn't hallucinate.
    if draft_existed is False:
    
        # place all fields here, this is to show the user what all details are needed to add an employee
        remaining_fields = ["full_name", "contact_number", "company_name", "role", "work_policy_name", "office_location_name", "department_name", "reporting_manager_name", "emailId", "designation", "dateOfJoining", "dateOfBirth", "gender", "reminders", "is_hr", "hr_scope"]
        if employee_record.group_id is None:
            remaining_fields.remove("hr_scope")
            EmployeeSessionProxy.add_to_list(contact_number=contact_number, items=["hr_scope"])
        # remove whatever fields are extracted from the user message
        for field in extracted_data.model_dump(exclude_none=True):
            if field in remaining_fields:
                print(f"Removing field: {field}")
                remaining_fields.remove(field)
                if field == "is_hr" or field == "hr_scope" or field == "reminders":
                    EmployeeSessionProxy.add_to_list(contact_number=contact_number, items=[field])
        explanations["add_employee_onboarding"] = Explanations.ADD_EMPLOYEE_ONBOARDING
        if "reminders" in remaining_fields:
            explanations["reminders"] = Explanations.REMINDERS

    # If in the list of fields being passed to the LLM contains office location, then we pass the explanation of office explanation
    # We also pass explanation for multiple office or single office based on the users group and company.
    if "office_location_name" in remaining_fields:
        office_list = EmployeeProxy.get_companies_by_group_and_company(group_id=employee_record.group_id, company_id=employee_record.company_id)
        explanations["office_location_name"] = Explanations.OFFICE_LOCATION
        if len(office_list) > 1:
            #add the office location names to the explanations
            explanations["office_location_names_the user_can_choose_from"] = office_list
            explanations["office_locations_checkin"] = Explanations.MULTIPLE_OFFICE_LOCATIONS
        else:
            explanations["office_location_checkin"] = Explanations.SINGLE_OFFICE_LOCATION

    # We pass these explanation if these fields are present
    if "reminders" in remaining_fields:
        explanations["reminders"] = Explanations.REMINDERS
    if "is_hr" in remaining_fields:
        explanations["is_hr"] = Explanations.IS_HR
    if "hr_scope" in remaining_fields:
        explanations["hr_scope"] = Explanations.HR_SCOPE

    print(f"Error Dict: {error_dict}")
    # only pass the last 2 messages to the extraction agent
    print(f"Extraction Messages: {extraction_messages[-2:]}")
    print(f"Remaining Fields: {remaining_fields}")
    print(f"Explanations: {explanations}")
    print(f"draft existed? : ",draft_existed)
    response = get_employee_details(messages=extraction_messages, fields=remaining_fields, error_dict=error_dict, explanations=explanations)
    EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
    LeadMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
    print(f"Assistant: {response.message_to_user}")

        
while True:
    user_input = input("User: ")
    create_employee(contact_number="+971512345678", user_message=user_input)

       


        