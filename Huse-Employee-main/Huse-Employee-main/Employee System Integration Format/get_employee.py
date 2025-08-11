from Utils.agents import get_employee_search_extraction, get_employee_chat
from Utils.fields_to_get import clean_employee_fields, format_employee_details
from Utils.sanitization import sanitize_messages
from proxies.employee_message_proxy import LeadMessageHistoryProxy
from proxies.proxy import EmployeeProxy
from proxies.employee_session_proxy import EmployeeSessionProxy
from Utils.dummy_functions import send_whatsapp_message, sendLLMResponse, generate_llm_response

def get_employee_records(contact_number: str, user_message: str):

    print("Entered Get Employee Records")

    LeadMessageHistoryProxy.save_message(contact_number, "user", user_message)

    error_dict = {}
    messages = LeadMessageHistoryProxy.get_message_history(contact_number)
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
    

    # Get the session ID from the database using the contact number
    EmployeeSessionProxy.add_message(contact_number, {"role": "user", "content": user_message})
    session_messages = EmployeeSessionProxy.get_messages(contact_number)
    print(f"Session Messages: {session_messages}")

    response = get_employee_search_extraction(session_messages, employee_record)
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
            # Add each employee result directly to the list
            all_results.extend(result)
            print(f"Criterion {i} ({criterion[0]}='{criterion[1]}'): Found {len(result)} employees")
        if error:
            error_dict.update(error)
    
    print(f"TOTAL EMPLOYEES FOUND: {len(all_results)}")

    
    EmployeeSessionProxy.clear_messages(contact_number)
    # EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
    print(f"Employee Record: {employee_info.company_id}")
    print(f"All Results: {all_results}")
    print(f"User Message: {user_message}")
    print(f"Contact Number: {contact_number}")
    response = sendLLMResponse(employee_info, generate_llm_response(employee_info.company_id, all_results, user_message, contact_number))
    LeadMessageHistoryProxy.save_message(contact_number, "assistant", response)
    return

while True:
    user_input = input("User: ")
    get_employee_records(contact_number="+971509876543", user_message=user_input)