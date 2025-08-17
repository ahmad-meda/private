from Utils.agents import soft_delete_employee_extraction, soft_delete_employee_response
from Utils.choices import EmployeeChoices
from Utils.fuzzy_logic import find_best_match
from Utils.formats import SoftDeleteExtraction  
from proxies.employee_session_proxy import EmployeeSessionProxy
from proxies.proxy import EmployeeProxy
from Utils.fields_to_delete import agent_states
from proxies.employee_message_proxy import LeadMessageHistoryProxy
from Utils.sanitization import sanitize_messages





def soft_delete_employee(contact_number, user_message:str):

    print("Entered Soft Delete Employee")

    LeadMessageHistoryProxy.save_message(contact_number, "user", user_message)

    # Get the Sales Agent ID from thedatabase using the contact number
    agent_id, agent_name = EmployeeProxy.get_hr_id_by_contact(contact_number=contact_number)
    print(f"HR Database ID: {agent_id}")
    
    error_dict = {}

    EmployeeSessionProxy.add_message(contact_number, {"role": "user", "content": user_message})
    session_messages = EmployeeSessionProxy.get_messages(contact_number)

    messages = LeadMessageHistoryProxy.get_message_history(contact_number)
    extraction_messages = sanitize_messages(messages)
    # print(f"Extraction Messages: {extraction_messages}")
    LeadMessageHistoryProxy.save_message(contact_number, "user", user_message)
    # Get updated messages after user input
    messages = LeadMessageHistoryProxy.get_message_history(contact_number)
    extraction_messages = sanitize_messages(messages)

    employee_record = EmployeeProxy.get_employee_record(contact_number=contact_number)

    print(f"Extraction Messages: {session_messages}")

    extracted_data = soft_delete_employee_extraction(messages=session_messages[-2:])
    print(f"Extracted Data: {extracted_data}")            
    
    if extracted_data.employee_name:
        extracted_data.employee_name = find_best_match(user_input=extracted_data.employee_name, choices=EmployeeChoices.get_all_employee_names(), threshold=85)
        employee_name = EmployeeProxy.get_employee_id_by_name(name=extracted_data.employee_name, hr_group_id=employee_record.group_id, hr_company_id=employee_record.company_id)
        if employee_name["success"] == False and employee_name["matches"] != []:
            print(f"Multiple Matches Found: {employee_name['matches']}")
            error_dict = employee_name["error"] if isinstance(employee_name["error"], dict) else {"error": employee_name["error"]}
        elif employee_name["success"] == False:
            print(f"Error: {employee_name['error']}")
            error_dict = employee_name["error"] if isinstance(employee_name["error"], dict) else {"error": employee_name["error"]}
        else:
            employee_id = employee_name["database_id"]
            result = EmployeeProxy._soft_delete_employee(database_id=employee_id)
            if result == False:
                print("Employee is already deleted")
                return
            print(f"Employee Soft Deleted: {employee_id}")
            EmployeeSessionProxy.clear_messages(contact_number)
            return

    if extracted_data.contact_number:
        employee_id = EmployeeProxy.get_employee_id_by_contact(contact_number=extracted_data.contact_number, hr_group_id=employee_record.group_id, hr_company_id=employee_record.company_id)
        if employee_id["success"] == False:
            print(f"Error: {employee_id['error']}")
            error_dict = employee_id["error"] if isinstance(employee_id["error"], dict) else {"error": employee_id["error"]}
        else:
            employee_id = employee_id["database_id"]
            result = EmployeeProxy._soft_delete_employee(database_id=employee_id)
            if result == False:
                print("Employee is already deleted")
                return
            print(f"Employee Soft Deleted: {employee_id}")
            EmployeeSessionProxy.clear_messages(contact_number) 
            return

    if extracted_data.contact_number or extracted_data.employee_name:
        agent_states.mandatory_fields = []

    response = soft_delete_employee_response(messages=session_messages[-1:], fields=agent_states.mandatory_fields, error_dict=error_dict)
    EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
    LeadMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
    print(f"Assistant: {response.message_to_user}")

while True:
    user_input = input("User: ")
    soft_delete_employee(contact_number="+971501234567", user_message=user_input)
