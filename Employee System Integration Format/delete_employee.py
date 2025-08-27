from Utils.agents import soft_delete_employee_extraction, soft_delete_employee_response
from Utils.choices import EmployeeChoices
from Utils.fuzzy_logic import find_best_match
from Utils.formats import SoftDeleteExtraction  
from proxies.employee_session_proxy import EmployeeSessionProxy
from proxies.proxy import EmployeeProxy
from Utils.fields_to_delete import agent_states
from proxies.employee_message_proxy import LeadMessageHistoryProxy
from Utils.dummy_functions import send_whatsapp_message, clear_session


def soft_delete_employee(contact_number, user_message:str):

    print("Entered Soft Delete Employee")

    LeadMessageHistoryProxy.save_message(contact_number, "user", user_message)
    EmployeeSessionProxy.add_message(contact_number, {"role": "user", "content": user_message})

    # Get the Sales Agent ID from thedatabase using the contact number
    agent_id, agent_name = EmployeeProxy.get_hr_id_by_contact(contact_number=contact_number)
    print(f"HR Database ID: {agent_id}")
    # Employee record that will return the entire employee object with all the employee details
    employee_record = EmployeeProxy.get_employee_record(contact_number=contact_number)
    
    # Error dictionary that will contain all errors when the extracted values are passed to the service functions.
    error_dict = {}

    # Session history using Redis.
    session_messages = EmployeeSessionProxy.get_messages(contact_number)
    print(f"Message History: {session_messages}")

    # Here we extract the data required to locate the employee in the database.
    extracted_data = soft_delete_employee_extraction(messages=session_messages[-2:])
    print(f"Extracted Data: {extracted_data}")            
    
    # We try to identify the employee based on name or contact number.
    # if multiple employees with the same name are found, then the all those employees will be passed into the error dict, which in turn will be passed to the LLM.
    # The LLM will then present the user with the options to select the correct employee.

    if extracted_data.employee_name:

        # If only the name is given and 1 employee exists, it will be located, but if multiple employees exist
        # Then the LLM will present the user with the options to select the correct employee. the mail, number and name of each duplicate employee is presented to the user.
        # So when the user choose one of the employees, the name, contact and the email is extracted of the chosen employee.
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
            deleted_employee_name = EmployeeProxy.get_employee_record_by_id(employee_id)
            send_whatsapp_message(contact_number, f" Deleted: {deleted_employee_name.name} successfully!")
            EmployeeSessionProxy.clear_messages(contact_number)
            clear_session(contact_number)
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
            deleted_employee_name = EmployeeProxy.get_employee_record_by_id(employee_id)
            send_whatsapp_message(contact_number, f" Deleted: {deleted_employee_name.name} successfully!")
            EmployeeSessionProxy.clear_messages(contact_number) 
            clear_session(contact_number)
            return

    # If the employee is identified, we empty the list of fields that we pass to the LLM to task the user (In this case, name or phone number)
    if extracted_data.contact_number or extracted_data.employee_name:
        agent_states.mandatory_fields = []

    response = soft_delete_employee_response(messages=session_messages[-1:], fields=agent_states.mandatory_fields, error_dict=error_dict)
    EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
    LeadMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
    send_whatsapp_message(contact_number, response.message_to_user)
    print(f"Assistant: {response.message_to_user}")

while True:
    user_input = input("User: ")
    soft_delete_employee(contact_number="+971509784398", user_message=user_input)
