from proxies.proxy import EmployeeProxy
from Utils.agents import update_employee_response, update_employee_extraction, extract_data, locate_update_employee, update_employee_end_response, ask_user_what_else_to_update, update_employee_fields_only
from Utils.fields_to_delete import agent_states
from Utils.choices import EmployeeChoices
from Utils.fuzzy_logic import find_best_match
from proxies.proxy import EmployeeProxy
from proxies.employee_message_proxy import LeadMessageHistoryProxy
from Utils.sanitization import sanitize_messages
from proxies.employee_session_proxy import EmployeeSessionProxy
from Utils.name_separation import separate_name
from Utils.dummy_functions import send_whatsapp_message
from proxies.employee_session_proxy import EmployeeSessionProxy

def update_employee_fields(contact_number:str, user_message:str):

    LeadMessageHistoryProxy.save_message(contact_number, "user", user_message)

    # session_messages = LeadMessageHistoryProxy.get_message_history(contact_number)

    EmployeeSessionProxy.add_message(contact_number, {"role": "user", "content": user_message})
    session_messages = EmployeeSessionProxy.get_messages(contact_number)


    agent_id = EmployeeProxy.get_hr_id_by_contact(contact_number=contact_number)
    print(f"HR Database ID: {agent_id}")

    employee_record = EmployeeProxy.get_employee_record(contact_number=contact_number)
    print(f"Employee Record: {employee_record}")

    employee_identified = EmployeeSessionProxy.get_employee_identified(contact_number)
    employee_id = EmployeeSessionProxy.get_employee_id(contact_number)
    extracted_current_data = None
    list_of_fields_with_no_value = []

    print(f"Employee Identified: {employee_identified}")
    print(f"Employee ID: {employee_id}")
    error_dict = {}

    messages = LeadMessageHistoryProxy.get_message_history(contact_number)
    extraction_messages = sanitize_messages(messages)
    #-------------------------------- add result= {} and extracted_fields_and_values = []
    result = {}
    extracted_fields_and_values = []
    closing_session = False
    
    LeadMessageHistoryProxy.save_message(contact_number, "user", user_message)
    messages = LeadMessageHistoryProxy.get_message_history(contact_number)
    extraction_messages = sanitize_messages(messages)

    # Always extract current data for employee identification
    sanitized_messages = sanitize_messages(session_messages[-2:])
    if employee_identified is False:
        extracted_current_data = locate_update_employee(messages=sanitized_messages)
    
    
    extracted_data = update_employee_extraction(messages=sanitize_messages(session_messages[-2:]))

    if employee_identified == True:
        if extracted_data.work_policy_name or extracted_data.office_location_name or extracted_data.department_name or extracted_data.reporting_manager_name or extracted_data.role or extracted_data.company_name or extracted_data.full_name or extracted_data.gender:
            extracted_data.work_policy_name = find_best_match(user_input=extracted_data.work_policy_name, choices=EmployeeChoices.get_work_policy_choices(), threshold=85)
            # Do not fuzzy-match special sentinel values
            if extracted_data.office_location_name not in ("manager_skip", "home_coordinates"):
                extracted_data.office_location_name = find_best_match(user_input=extracted_data.office_location_name, choices=EmployeeChoices.get_office_location_choices(), threshold=85)
            extracted_data.department_name = find_best_match(user_input=extracted_data.department_name, choices=EmployeeChoices.get_departments_choices(), threshold=85)
            extracted_data.reporting_manager_name = find_best_match(user_input=extracted_data.reporting_manager_name, choices=EmployeeChoices.get_reporting_manager_choices(hr_company_id=employee_record.company_id, hr_group_id=employee_record.group_id), threshold=85)
            extracted_data.role = find_best_match(user_input=extracted_data.role, choices=EmployeeChoices.get_role_choices(), threshold=85)
            extracted_data.gender = find_best_match(user_input=extracted_data.gender, choices=EmployeeChoices.get_gender_choices(), threshold=85)
            extracted_data.company_name = find_best_match(user_input=extracted_data.company_name, choices=EmployeeChoices.get_companies_choices(group_id=employee_record.group_id, company_id=employee_record.company_id), threshold=85)
            extracted_data.first_name, extracted_data.middle_name, extracted_data.last_name = separate_name(extracted_data.full_name)
        print(f"Extracted Data: {extracted_data}")

    if employee_id is None:

        if extracted_current_data.current_name and employee_identified == False:
            matched_name = find_best_match(user_input=extracted_current_data.current_name, choices=EmployeeChoices.get_all_employee_names(), threshold=85)
            # FIX THIS --------------------------------
            employee_name = EmployeeProxy.get_employee_id_by_name(
                name=matched_name,
                email=extracted_current_data.current_email,
                contact_number=extracted_current_data.current_phone_number
            )
            if employee_name["success"] == False and employee_name["matches"] != []:
                print(f"Multiple Matches Found: {employee_name['matches']}")
                error_dict = employee_name["error"] if isinstance(employee_name["error"], dict) else {"error": employee_name["error"]}
            elif employee_name["success"] == False:
                print(f"Error: {employee_name['error']}")
                error_dict = employee_name["error"] if isinstance(employee_name["error"], dict) else {"error": employee_name["error"]}
            else:
                employee_id = employee_name["database_id"]
                employee_identified = True
                print(f"Employee Identified: {employee_id}")
                EmployeeSessionProxy.set_employee_identified(contact_number, True)
                EmployeeSessionProxy.set_employee_id(contact_number, employee_id)
                
        if extracted_current_data.current_phone_number and employee_identified == False:
            employee_contact_result = EmployeeProxy.get_employee_id_by_contact(contact_number=extracted_current_data.current_phone_number)
            if employee_contact_result["success"] == False:
                print(f"Error: {employee_contact_result['error']}")
                error_dict = {employee_contact_result["error"]}
            else:
                employee_id = employee_contact_result["database_id"]
                employee_identified = True
                print(f"Employee Identified: {employee_id}")
                EmployeeSessionProxy.set_employee_identified(contact_number, True)
                EmployeeSessionProxy.set_employee_id(contact_number, employee_id)
               

    #-------------------------------- ADD if_fields_present ----------FIX

    # Only attempt update if employee is identified and employee_id is valid
    if employee_identified and employee_id is not None:
        if_fields_present = extracted_data.model_dump(exclude_none=True)
        print(f"If Fields Present: {if_fields_present}")
        if if_fields_present:
            result = EmployeeProxy._update_employee_by_id(employee_db_id=employee_id,
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
            print(f"Result: {result}")
            error_dict = result["errors"]
            if error_dict == {}:
                closing_session = True
            extracted_fields_and_values = []
            for field, value in if_fields_present.items():
                extracted_fields_and_values.append(f"{field}: {value}")

    if employee_identified == True:

        print("--------------------------------IN EMPLOYEE IDENTIFIED LOOP--------------------------------")

        fields_mentioned = update_employee_fields_only(messages=extraction_messages[-2:])
        chosen_fields = [field for field in fields_mentioned.model_dump(exclude_none=True) if fields_mentioned.model_dump(exclude_none=True)[field]]
        print("fields with names:",chosen_fields)

        list_of_fields_with_no_value = [field for field in chosen_fields if field not in extracted_data.model_dump(exclude_none=True)]
        print(f"list_of_fields_to_update: {list_of_fields_with_no_value}")


        print("--------------------------------")
        print(f"Extracted Fields and Values: {extracted_fields_and_values}")
        print(f"Result: {result}")
        print(f"Fields chosen by user: {chosen_fields}")
        print(f"Fields with value: {list_of_fields_with_no_value}")
        print("--------------------------------")

        print(f"Error Dict: {error_dict}")
        response = ask_user_what_else_to_update(extracted_fields_and_values, result, list_of_fields_with_no_value)
        LeadMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
        # send_whatsapp_message(contact_number=contact_number, response=response.message_to_user)
        print(f"chat_assistant: {response}")
        if closing_session == True:
            LeadMessageHistoryProxy.clear_message_history(contact_number)
            EmployeeSessionProxy.clear_employee_session(contact_number)
            LeadMessageHistoryProxy.clear_message_history(contact_number)
            return response.message_to_user
    else:
        response = update_employee_response(messages=session_messages[-4:], employee_identified=employee_identified, error_dict=error_dict, fields=agent_states.mandatory_fields)
        LeadMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
        EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
        # send_whatsapp_message(contact_number=contact_number, response=response.message_to_user)
        print(f"chat_assistant: {response}")
while True:
    user_input = input("User: ")
    update_employee_fields(contact_number="+971512345678", user_message=user_input)