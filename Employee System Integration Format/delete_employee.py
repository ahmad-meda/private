from Utils.agents import ask_user_for_confirmation, soft_delete_employee_extraction, soft_delete_employee_response
from Utils.choices import EmployeeChoices
from Utils.fuzzy_logic import find_best_match
from Utils.formats import SoftDeleteExtraction  
from proxies.employee_session_proxy import EmployeeSessionProxy
from proxies.proxy import EmployeeProxy
from Utils.fields_to_delete import agent_states
from proxies.employee_message_proxy import EmployeeMessageHistoryProxy
from Utils.dummy_functions import send_whatsapp_message, clear_session
from Utils.delete_huse_user import delete_user_by_username

def soft_delete_employee(contact_number, user_message:str):

    print("Entered Soft Delete Employee")

    EmployeeMessageHistoryProxy.save_message(contact_number, "user", user_message)
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

    # This is to check if the user has asked for confirmation before deleting the employee.
    asked_confirmation = EmployeeSessionProxy.get_asked_confirmation(contact_number)

    if asked_confirmation == True:
        # Get the employee_id from Redis that was saved earlier
        employee_id = EmployeeSessionProxy.get_employee_id(contact_number)
        
        llm_response = ask_user_for_confirmation(messages=session_messages[-2:])

        if llm_response.does_user_want_to_delete == True:
            result = EmployeeProxy._soft_delete_employee(database_id=employee_id)
            if result == False:
                print("Employee is already deleted")
                error_message = "This employee has already been deleted."
                EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", error_message)
                send_whatsapp_message(contact_number, error_message)
                return
            elif result is None:
                print("ERROR: Failed to delete employee from database")
                error_message = "Sorry, there was an error deleting the employee from the database. Please try again or contact support."
                EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", error_message)
                EmployeeSessionProxy.clear_messages(contact_number)
                EmployeeSessionProxy.clear_asked_confirmation(contact_number)
                EmployeeSessionProxy.clear_employee_session(contact_number)
                send_whatsapp_message(contact_number, error_message)
                clear_session(contact_number)
                return
            print(f"Employee Soft Deleted: {employee_id}")
            deleted_employee_name = EmployeeProxy.get_employee_record_by_id(employee_id)

            employee_username = deleted_employee_name.username
            if employee_username:
                huse_response = delete_user_by_username(employee_username)
                print(f"Huse Response: {huse_response}")
            else:
                print(f"Employee is not registered in Huse")
                
            send_whatsapp_message(contact_number, f" Deleted: {deleted_employee_name.name} successfully!")
            # Clear the employee_id and asked_confirmation from Redis after successful deletion
            EmployeeSessionProxy.clear_employee_session(contact_number)
            EmployeeSessionProxy.clear_asked_confirmation(contact_number)
            EmployeeSessionProxy.clear_messages(contact_number) 
            clear_session(contact_number)
            print(" --------------------- MESSAGES CLEARED --------------------- ")
            print(" --------------------- SESSION CLEARED --------------------- ")
            print(" --------------------- CONFIRMATION VARIABLE CLEARED --------------------- ")
            print(" --------------------- EMPLOYEE ID CLEARED --------------------- ")
            return

        else:

            if llm_response.did_user_mention_another_employee:
                print(f"Name of Employee: {llm_response.did_user_mention_another_employee}")
                EmployeeSessionProxy.set_asked_confirmation(contact_number, False)
            
            else:
                send_whatsapp_message(contact_number, llm_response.farewell_message_to_user)
                EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", llm_response.farewell_message_to_user)
                EmployeeSessionProxy.clear_employee_session(contact_number)
                EmployeeSessionProxy.clear_asked_confirmation(contact_number)
                EmployeeSessionProxy.clear_messages(contact_number) 
                clear_session(contact_number)
                print(" --------------------- MESSAGES CLEARED --------------------- ")
                print(" --------------------- SESSION CLEARED --------------------- ")
                print(" --------------------- CONFIRMATION VARIABLE CLEARED --------------------- ")
                print(" --------------------- EMPLOYEE ID CLEARED --------------------- ")
                return


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
        extracted_data.employee_name = find_best_match(user_input=extracted_data.employee_name, choices=EmployeeChoices.get_all_employee_names(), threshold=95)
        employee_name = EmployeeProxy.get_employee_id_by_name(name=extracted_data.employee_name, hr_group_id=employee_record.group_id, hr_company_id=employee_record.company_id)
        if employee_name["success"] == False and employee_name["matches"] != []:
            print(f"Multiple Matches Found: {employee_name['matches']}")
            error_dict = employee_name["error"] if isinstance(employee_name["error"], dict) else {"error": employee_name["error"]}
        elif employee_name["success"] == False:
            print(f"Error: {employee_name['error']}")
            error_dict = employee_name["error"] if isinstance(employee_name["error"], dict) else {"error": employee_name["error"]}
        else:
            employee_id = employee_name["database_id"]
            # Save employee_id to Redis for later use
            EmployeeSessionProxy.set_employee_id(contact_number, employee_id)
            EmployeeSessionProxy.set_asked_confirmation(contact_number, True)
            to_delete_employee_record = EmployeeProxy.get_employee_record_by_id(employee_id)
            confirmation_message = f"Are you sure you want to delete {to_delete_employee_record.name} from the database?\nHere are few details about the employee to make sure we have the right person:\n*Full Name*: {to_delete_employee_record.name}\n*Contact Number*: {to_delete_employee_record.contactNo}\n*Email*: {to_delete_employee_record.emailId}"
            send_whatsapp_message(contact_number, confirmation_message)
            EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", confirmation_message)
            EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": confirmation_message})
            return


    if extracted_data.contact_number:
        employee_id = EmployeeProxy.get_employee_id_by_contact(contact_number=extracted_data.contact_number, hr_group_id=employee_record.group_id, hr_company_id=employee_record.company_id)
        if employee_id["success"] == False:
            print(f"Error: {employee_id['error']}")
            error_dict = employee_id["error"] if isinstance(employee_id["error"], dict) else {"error": employee_id["error"]}
        else:
            employee_id = employee_id["database_id"]
            # Save employee_id to Redis for later use
            EmployeeSessionProxy.set_employee_id(contact_number, employee_id)
            to_delete_employee_record = EmployeeProxy.get_employee_record_by_id(employee_id)
            EmployeeSessionProxy.set_asked_confirmation(contact_number, True)
            confirmation_message = f"Are you sure you want to delete {to_delete_employee_record.name} from the database?\nHere are few details about the employee to make sure we have the right person:\n*Full Name*: {to_delete_employee_record.name}\n*Contact Number*: {to_delete_employee_record.contactNo}\n*Email*: {to_delete_employee_record.emailId}"
            send_whatsapp_message(contact_number, confirmation_message)
            EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", confirmation_message)
            EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": confirmation_message})
            return

    # If the employee is identified, we empty the list of fields that we pass to the LLM to task the user (In this case, name or phone number)
    if extracted_data.contact_number or extracted_data.employee_name:
        agent_states.mandatory_fields = []

    response = soft_delete_employee_response(messages=session_messages[-1:], fields=agent_states.mandatory_fields, error_dict=error_dict)
    EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
    EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
    send_whatsapp_message(contact_number, response.message_to_user)
    print(f"Assistant: {response.message_to_user}")
    return