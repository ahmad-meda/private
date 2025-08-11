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

def create_employee(contact_number:str, user_message:str):

    print("Entered Create Employee")

    skip_optional_logic = False

    LeadMessageHistoryProxy.save_message(contact_number, "user", user_message)

     # Get the Sales Agent ID from thedatabase using the contact number
    agent_id, agent_name = EmployeeProxy.get_hr_id_by_contact(contact_number=contact_number)

    draft_table_id, draft_id, draft_existed = EmployeeProxy.get_draft(agent_id, DraftType.EMPLOYEE.value)

    main_fields, optional_personal_fields, optional_employment_fields, optional_location_fields = get_null_fields(draft_id)

    employee_record = EmployeeProxy.get_employee_record(contact_number=contact_number)
    print(f"Employee Record: {employee_record.company_id} {employee_record.group_id}") 

    print(f"Main Fields: {main_fields}")
    print(f"Optional Personal Fields: {optional_personal_fields}")
    print(f"Optional Employment Fields: {optional_employment_fields}")
    print(f"Optional Location Fields: {optional_location_fields}")

    session_fields = EmployeeSessionProxy.get_list(contact_number=contact_number)
    print(f"Session Fields: {session_fields}")

    #  if current field is main_fields.
    current_phase, remaining = remove_fields_by_name_and_return_next(used_fields=session_fields,
                                          mandatory_fields=main_fields,
                                          optional_personal_fields=optional_personal_fields,
                                          optional_employment_fields=optional_employment_fields,
                                          optional_location_fields=optional_location_fields)

    error_dict = {}
    explanations = {}  # Clear explanations at the start of each iteration

    messages = LeadMessageHistoryProxy.get_message_history(contact_number)
    extraction_messages = sanitize_messages(messages)


    LeadMessageHistoryProxy.save_message(contact_number, "user", user_message)
    # Get updated messages after user input
    messages = LeadMessageHistoryProxy.get_message_history(contact_number)
    extraction_messages = sanitize_messages(messages)

    # print(f"Extraction Messages: {extraction_messages}")
    extracted_data = extract_data(messages=extraction_messages[-2:])
    print(f"Extracted Data: {extracted_data}")

    if extracted_data.full_name or extracted_data.work_policy_name or extracted_data.office_location_name or extracted_data.department_name or extracted_data.reporting_manager_name or extracted_data.role or extracted_data.company_name or extracted_data.gender :
        extracted_data.work_policy_name = find_best_match(user_input=extracted_data.work_policy_name, choices=EmployeeChoices.get_work_policy_choices(), threshold=85)
        extracted_data.office_location_name = find_best_match(user_input=extracted_data.office_location_name, choices=EmployeeChoices.get_office_location_choices(), threshold=90)
        extracted_data.department_name = find_best_match(user_input=extracted_data.department_name, choices=EmployeeChoices.get_departments_choices(), threshold=85)
        extracted_data.reporting_manager_name = find_best_match(user_input=extracted_data.reporting_manager_name, choices=EmployeeChoices.get_reporting_manager_choices(hr_company_id=employee_record.company_id, hr_group_id=employee_record.group_id), threshold=85)
        extracted_data.role = find_best_match(user_input=extracted_data.role, choices=EmployeeChoices.get_role_choices(), threshold=85)
        extracted_data.company_name = find_best_match(user_input=extracted_data.company_name, choices=EmployeeChoices.get_companies_choices(), threshold=85)
        extracted_data.gender = find_best_match(user_input=extracted_data.gender, choices=EmployeeChoices.get_gender_choices(), threshold=85)
        extracted_data.first_name, extracted_data.middle_name, extracted_data.last_name = separate_name(extracted_data.full_name)
    
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
                                                hr_company_id=employee_record.company_id,
                                                hr_group_id=employee_record.group_id)
        
        # Validate the updating of the draft - If there is an error in updating a certain field, that field of the extracted data will be set to None
        error_dict = result['errors']
        print(f"Error Dict: {error_dict}")

       # If there are errors in any fields, set those fields to None
    for field_name in error_dict:
        if hasattr(extracted_data, field_name):
            setattr(extracted_data, field_name, None)
            

    
    main_fields, optional_personal_fields, optional_employment_fields, optional_location_fields = get_null_fields(draft_id)

    session_fields = EmployeeSessionProxy.get_list(contact_number=contact_number)
    print(f"Session Fields: {session_fields}")

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

    #only enter this if the current field is not a mandatory field
    if current_field != "mandatory_fields" and skip_optional_logic == True:
        print("currently in optional fields")
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
    
    
    
    if current_field is None and len(remaining_fields) == 0:
        print("Adding in main database")
        EmployeeProxy._add_employee_in_main_database(draft_id=draft_id)
        EmployeeProxy._delete_draft(draft_id=draft_table_id)
        LeadMessageHistoryProxy.clear_message_history(contact_number)
        EmployeeSessionProxy.clear_list(contact_number=contact_number)
        return

    if "office_location_name" in remaining_fields:
        explanations["office_location_name"] = Explanations.OFFICE_LOCATION

    print(f"Error Dict: {error_dict}")
    # only pass the last 2 messages to the extraction agent
    print(f"Extraction Messages: {extraction_messages[-2:]}")
    print(f"Remaining Fields: {remaining_fields}")
    response = get_employee_details(messages=extraction_messages, fields=remaining_fields, error_dict=error_dict, explanations=explanations)
    LeadMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
    print(f"Assistant: {response.message_to_user}")

        
while True:
    user_input = input("User: ")
    create_employee(contact_number="+971509876543", user_message=user_input)

       


        