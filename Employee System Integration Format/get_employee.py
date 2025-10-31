from Utils.agents import get_employee_search_extraction, get_employee_chat
from Utils.fields_to_get import clean_employee_fields, format_employee_details
from Utils.sanitization import sanitize_messages
from proxies.employee_message_proxy import EmployeeMessageHistoryProxy
from proxies.proxy import EmployeeProxy
from proxies.employee_session_proxy import EmployeeSessionProxy
from Utils.dummy_functions import clear_session, send_whatsapp_message
import re

def get_employee_records(contact_number: str, user_message: str):

    print("Entered Get Employee Records")

    EmployeeMessageHistoryProxy.save_message(contact_number, "user", user_message)

    error_dict = {}
    messages = EmployeeMessageHistoryProxy.get_message_history(contact_number)
    extraction_messages = sanitize_messages(messages)

    # Get the Sales Agent ID from thedatabase using the contact number
    agent_id, agent_name = EmployeeProxy.get_hr_id_by_contact(contact_number=contact_number)
    print(f"HR Database ID: {agent_id}")
    print(f"HR Name: {agent_name}")

    # Get the employee record from the database using the contact number
    employee_info = EmployeeProxy.get_employee_record(contact_number=contact_number)
    print(f"Employee Record: {employee_info}")
    print(employee_info.company_id)
    employee_record = EmployeeProxy.get_employee_by_contact_number(contact_number=contact_number)
    print(f"Employee Record with names: {employee_record}")
    print(f"Employee Record Contact Number: {employee_info.contactNo}")
    

    # Get the session ID from the database using the contact number
    EmployeeSessionProxy.add_message(contact_number, {"role": "user", "content": user_message})
    session_messages = EmployeeSessionProxy.get_messages(contact_number)
    print(f"Session Messages: {session_messages}")

    response = get_employee_search_extraction(session_messages, employee_record=employee_info)
    print(response.model_dump(exclude_none=True))
    print(response.fields)
    print(f"All Fields Given: {response.all_fields_given}")
    if response.all_fields_given != True:
        print(f"Agent: {response.message_to_user}")
        EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
        return
    
    # Clean the extracted fields
    criteria_list = clean_employee_fields(response)
    print(f"Criteria List: {criteria_list}")

    # Use a simple loop to handle each criterion separately
    all_results = []
    error_dict = {}
    
    for i, criterion in enumerate(criteria_list, 1):
        result, error = EmployeeProxy.get_employee_by_criteria([criterion], employee_info.company_id, employee_info.group_id)
        if result:
            # Structure results by criterion
            field_name, field_value = criterion
            # If searching by contact number and it matches the user's contact, use "user_profile"
            normalized_contact = None if contact_number is None else re.sub(r'[^\d]', '', str(contact_number))
            if field_name == 'contactNo' and field_value == normalized_contact:
                criterion_key = "user_profile"
            else:
                criterion_key = f"employees_with_{field_name}_{field_value}"
            all_results.append({criterion_key: result})
            print(f"Criterion {i} ({criterion[0]}='{criterion[1]}'): Found {len(result)} employees")
        if error:
            error_dict.update(error)
    
    print(f"TOTAL EMPLOYEES FOUND: {sum(len(list(result.values())[0]) for result in all_results)}")

    if len(all_results) == 0:
        no_employee_message = "I'm sorry, but I couldn't find any employees matching your search criteria. Please try adjusting your search parameters or contact your HR department for assistance."
        print(f"No employees found. Sending message: {no_employee_message}")
        EmployeeSessionProxy.clear_messages(contact_number)
        EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", no_employee_message)
        send_whatsapp_message(contact_number, no_employee_message)
        clear_session(contact_number)
        return

    EmployeeSessionProxy.clear_messages(contact_number)
    # EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
    print(f"Employee Record: {employee_info.company_id}")
    print(f"All Results: {all_results}")
    print(f"User Message: {user_message}")
    print(f"Contact Number: {contact_number}")
    # response = sendLLMResponse(employee_info, generate_llm_response(employee_info.company_id, all_results, user_message, contact_number))
    # print(f"Extraction Messages: {extraction_messages}")
    response = get_employee_chat(extraction_messages[-1:], error_dict, employee_details=all_results)
    EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
    send_whatsapp_message(contact_number, response.message_to_user)

    clear_session(contact_number)
    EmployeeSessionProxy.clear_messages(contact_number)
    # EmployeeMessageHistoryProxy.clear_message_history(contact_number)
    return

while True:
    user_input = input("User: ")
    get_employee_records(contact_number="+971512345678", user_message=user_input)