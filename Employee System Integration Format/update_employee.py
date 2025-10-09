from proxies.proxy import EmployeeProxy
from Utils.agents import ask_user_for_confirmation_to_update_employee, update_employee_response, update_employee_extraction, extract_data, locate_update_employee, update_employee_end_response, ask_user_what_else_to_update, update_employee_fields_only
from Utils.fields_to_delete import agent_states
from Utils.choices import EmployeeChoices
from Utils.fuzzy_logic import find_best_match
from proxies.proxy import EmployeeProxy
from proxies.employee_message_proxy import EmployeeMessageHistoryProxy
from Utils.sanitization import sanitize_messages
from proxies.employee_session_proxy import EmployeeSessionProxy
from Utils.name_separation import separate_name
from Utils.dummy_functions import send_whatsapp_message
from proxies.employee_session_proxy import EmployeeSessionProxy
from Utils.dummy_functions import send_whatsapp_message, clear_session
from Utils.update_extraction_values import get_filled_fields

def update_employee_fields(contact_number:str, user_message:str):

    # Save the user message in Postgres db and Redis session
    EmployeeMessageHistoryProxy.save_message(contact_number, "user", user_message)
    EmployeeSessionProxy.add_message(contact_number, {"role": "user", "content": user_message})

    # Get the previous messages of the conversation from redis session
    session_messages = EmployeeSessionProxy.get_messages(contact_number)
    print(f"Session Messages: {session_messages}")

    # Get the user (HR) details from the db.
    agent_id = EmployeeProxy.get_hr_id_by_contact(contact_number=contact_number)
    print(f"HR Database ID: {agent_id}")
    employee_record = EmployeeProxy.get_employee_record(contact_number=contact_number)
    print(f"Employee Record: {employee_record}")

    # Check if the employee that the user wants to update has been located in the database, we get this variable from redis session
    # We store the variable in redis as we run this function in iteration.
    employee_identified = EmployeeSessionProxy.get_employee_identified(contact_number)
    employee_id = EmployeeSessionProxy.get_employee_id(contact_number)
    extracted_current_data = None

    extracted_not_confirmed = {}

    # This is to identify when the user mentions a field but doesn't mention the new value of the field he wants to update.
    list_of_fields_with_no_value = []

    print(f"Employee Identified: {employee_identified}")
    print(f"Employee ID: {employee_id}")

    # Our error dictionary that will contain all errors when the extracted values are passed to the service functions.
    error_dict = {}

    # This is to store the result of the update employee service function.
    result = {}
    # This is to store the fields and values that the user has mentioned in the message.
    extracted_fields_and_values = []
    # We use this boolean to check if the session is closing.
    closing_session = False
    
    EmployeeMessageHistoryProxy.save_message(contact_number, "user", user_message)
    messages = EmployeeMessageHistoryProxy.get_message_history(contact_number)
    extraction_messages = sanitize_messages(messages)

    # Always extract current data for employee identification
    sanitized_messages = sanitize_messages(session_messages[-2:])

    does_user_want_to_exit = update_employee_end_response(messages=session_messages[-2:])
    if does_user_want_to_exit.does_user_want_end_interaction is True:
        print(f"User wants to exit: {does_user_want_to_exit.farwell_message_to_user}")
        EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", does_user_want_to_exit.farwell_message_to_user)
        send_whatsapp_message(contact_number, does_user_want_to_exit.farwell_message_to_user)
        EmployeeSessionProxy.clear_employee_session(contact_number)
        EmployeeSessionProxy.clear_messages(contact_number)
        EmployeeSessionProxy.clear_update_agent_confirmation(contact_number)
        EmployeeSessionProxy.clear_field_confirmation_list(contact_number)
        clear_session(contact_number)
        return

    if employee_identified is False:
        extracted_current_data = locate_update_employee(messages=session_messages)

     # Extracted data after the employee has been identified.
    extracted_data = update_employee_extraction(messages=session_messages[-2:])

    # Check if the extracted data is same in the database, if so then make it null.
    if employee_identified and employee_id is not None:
        # Get employee details for comparison
        employee_details = EmployeeProxy.get_employee_record_by_id(employee_id)
        if employee_details:
            # Get current field values from database using the same format as extraction
            current_db_fields = get_filled_fields(employee_details)
            
            # Filter out unchanged fields by setting them to None
            extracted_fields = extracted_data.model_dump(exclude_none=True)
            
            for field, value in extracted_fields.items():
                # Get the current value from database
                current_value = current_db_fields.get(field)
                
                # Convert both values to strings for comparison (handle None values)
                current_str = str(current_value) if current_value is not None else ""
                new_str = str(value) if value is not None else ""
                
                # If values are the same, set the field to None
                if current_str.lower().strip() == new_str.lower().strip():
                    setattr(extracted_data, field, None)
                    print(f"Field '{field}' unchanged: '{current_str}' (set to None)")
                else:
                    print(f"Field '{field}' changed: '{current_str}' → '{new_str}'")
    
    if_fields_present = extracted_data.model_dump(exclude_none=True)
    print(f"If Fields Present (after filtering): {if_fields_present}") 
    

    #-----Confirmation loop-----
    asked_confirmation_to_update = EmployeeSessionProxy.get_update_agent_confirmation(contact_number=contact_number)
    print(f"Asked Confirmation to Update: {asked_confirmation_to_update}")
    if asked_confirmation_to_update == True:
        llm_response = ask_user_for_confirmation_to_update_employee(messages=session_messages[-2:])
        print(f"LLM Response: {llm_response}")
        if llm_response.does_user_want_to_update_the_employee == True:
            print("Updating in main database")
            
            # Get the fields that are in the Redis confirmation list
            confirmed_fields = EmployeeSessionProxy.get_field_confirmation_list(contact_number)
            print(f"Fields in Redis confirmation list: {confirmed_fields}")
            #-----------------------------------------
            # Simple variable: extracted fields NOT in confirmed fields
            extracted_not_confirmed = {field: value for field, value in if_fields_present.items() if field not in confirmed_fields}
            print(f"Extracted but not confirmed: {extracted_not_confirmed}")
            
            # Only send fields that are in the confirmation list to the update method
            update_result = EmployeeProxy._update_employee_by_id(employee_db_id=employee_id,
                                                    employee_id=extracted_data.employee_id if "employee_id" in confirmed_fields else None,
                                                    full_name=extracted_data.full_name if "full_name" in confirmed_fields else None, 
                                                    contact_number=extracted_data.contact_number if "contact_number" in confirmed_fields else None,
                                                    company_name=extracted_data.company_name if "company_name" in confirmed_fields else None, 
                                                    role=extracted_data.role if "role" in confirmed_fields else None, 
                                                    work_policy_name=extracted_data.work_policy_name if "work_policy_name" in confirmed_fields else None, 
                                                    office_location_name=extracted_data.office_location_name if "office_location_name" in confirmed_fields else None, 
                                                    department_name=extracted_data.department_name if "department_name" in confirmed_fields else None, 
                                                    reporting_manager_name=extracted_data.reporting_manager_name if "reporting_manager_name" in confirmed_fields else None, 
                                                    first_name=extracted_data.first_name if "first_name" in confirmed_fields else None, 
                                                    middle_name=extracted_data.middle_name if "middle_name" in confirmed_fields else None, 
                                                    last_name=extracted_data.last_name if "last_name" in confirmed_fields else None, 
                                                    emailId=extracted_data.emailId if "emailId" in confirmed_fields else None, 
                                                    designation=extracted_data.designation if "designation" in confirmed_fields else None, 
                                                    dateOfJoining=extracted_data.dateOfJoining if "dateOfJoining" in confirmed_fields else None, 
                                                    dateOfBirth=extracted_data.dateOfBirth if "dateOfBirth" in confirmed_fields else None, 
                                                    gender=extracted_data.gender if "gender" in confirmed_fields else None, 
                                                    home_latitude=extracted_data.home_latitude if "home_latitude" in confirmed_fields else None, 
                                                    home_longitude=extracted_data.home_longitude if "home_longitude" in confirmed_fields else None,
                                                    allow_site_checkin=extracted_data.allow_site_checkin if "allow_site_checkin" in confirmed_fields else None,
                                                    restrict_to_allowed_locations=extracted_data.restrict_to_allowed_locations if "restrict_to_allowed_locations" in confirmed_fields else None,
                                                    reminders=extracted_data.reminders if "reminders" in confirmed_fields else None,
                                                    is_hr=extracted_data.is_hr if "is_hr" in confirmed_fields else None,
                                                    hr_scope=extracted_data.hr_scope if "hr_scope" in confirmed_fields else None,
                                                    hr_company_id=employee_record.company_id,
                                                    hr_group_id=employee_record.group_id)
            print(f"Update Result: {update_result}")
            error_dict = update_result.get("errors", {}) if isinstance(update_result, dict) else {}
            if error_dict == {}:
                closing_session = True
                # Clear the confirmation status after successful update
                # EmployeeSessionProxy.clear_update_agent_confirmation(contact_number)
                # Remove the successfully updated fields from the confirmation list
            for field in confirmed_fields.keys():
                EmployeeSessionProxy.remove_field_from_confirmation_list(contact_number, field)
            extracted_fields_and_values = []
            for field, value in if_fields_present.items():
                extracted_fields_and_values.append(f"{field}: {value}")

            fields_mentioned = update_employee_fields_only(messages=session_messages[-1:])
            chosen_fields = [field for field in fields_mentioned.model_dump(exclude_none=True) if fields_mentioned.model_dump(exclude_none=True)[field]]
            print("fields with names:",chosen_fields)

            list_of_fields_with_no_value = [field for field in chosen_fields if field not in extracted_data.model_dump(exclude_none=True)]
            print(f"list_of_fields_to_update: {list_of_fields_with_no_value}")

            # We print the extracted fields and values, result, fields chosen by user, fields with value and error dict.
            print("--------------------------------")
            print(f"Extracted Fields and Values: {extracted_fields_and_values}")
            print(f"Update Result: {update_result}")
            print(f"Fields chosen by user: {chosen_fields}")
            print(f"Fields with without value: {list_of_fields_with_no_value}")
            print("--------------------------------")

            print(f"Error Dict: {error_dict}")

            print(f"Confirmed Fields: {confirmed_fields}")
            
            # Use the agent to generate appropriate response after update
            response = ask_user_what_else_to_update(extracted_fields_and_values, update_result, list_of_fields_with_no_value, fields_not_confirmed=extracted_not_confirmed)
            
            # Add extracted_not_confirmed fields to the confirmed fields list
            for field, value in extracted_not_confirmed.items():
                EmployeeSessionProxy.add_field_to_confirmation_list(contact_number, field, str(value))
            
            EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
            EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
            send_whatsapp_message(contact_number, response.message_to_user)
            print(f"chat_assistant: {response.message_to_user}")
            if extracted_not_confirmed == {}:
                EmployeeSessionProxy.clear_update_agent_confirmation(contact_number)
            if error_dict == {} and list_of_fields_with_no_value == [] and extracted_not_confirmed == {}:
                EmployeeSessionProxy.clear_update_agent_confirmation(contact_number)
                EmployeeSessionProxy.clear_messages(contact_number)
                EmployeeSessionProxy.clear_employee_session(contact_number)
                EmployeeSessionProxy.clear_field_confirmation_list(contact_number)
                clear_session(contact_number)
                print(" --------------------- MESSAGES CLEARED --------------------- ")
                print(" --------------------- SESSION CLEARED --------------------- ")
                print(" --------------------- CONFIRMATION VARIABLE CLEARED --------------------- ")
                print(" --------------------- EMPLOYEE ID CLEARED --------------------- ")
                print(" --------------------- FIELD CONFIRMATION LIST CLEARED --------------------- ")
                return
            return
        
        if llm_response.is_the_employee_to_update_wrong == True:
            EmployeeSessionProxy.set_employee_identified(contact_number, False)
            EmployeeSessionProxy.clear_employee_id(contact_number)
            EmployeeSessionProxy.clear_messages(contact_number)
            EmployeeSessionProxy.clear_employee_session(contact_number)
            EmployeeSessionProxy.clear_update_agent_confirmation(contact_number)
            EmployeeSessionProxy.clear_field_confirmation_list(contact_number)
            pass
        
            
    
    # Fuzzy logic to find the best match for the extracted data.
    if employee_identified == True:
        if extracted_data.work_policy_name or extracted_data.office_location_name or extracted_data.department_name or extracted_data.reporting_manager_name or extracted_data.role or extracted_data.company_name or extracted_data.full_name or extracted_data.gender:
            extracted_data.work_policy_name = find_best_match(user_input=extracted_data.work_policy_name, choices=EmployeeChoices.get_work_policy_choices(), threshold=85)
            extracted_data.office_location_name = find_best_match(user_input=extracted_data.office_location_name, choices=EmployeeChoices.get_office_location_choices(group_id=employee_record.group_id, company_id=employee_record.company_id), threshold=85)
            extracted_data.department_name = find_best_match(user_input=extracted_data.department_name, choices=EmployeeChoices.get_departments_choices(), threshold=85)
            extracted_data.reporting_manager_name = find_best_match(user_input=extracted_data.reporting_manager_name, choices=EmployeeChoices.get_reporting_manager_choices(hr_company_id=employee_record.company_id, hr_group_id=employee_record.group_id), threshold=85)
            extracted_data.role = find_best_match(user_input=extracted_data.role, choices=EmployeeChoices.get_role_choices(), threshold=85)
            extracted_data.gender = find_best_match(user_input=extracted_data.gender, choices=EmployeeChoices.get_gender_choices(), threshold=85)
            extracted_data.company_name = find_best_match(user_input=extracted_data.company_name, choices=EmployeeChoices.get_companies_choices(group_id=employee_record.group_id, company_id=employee_record.company_id), threshold=85)
            extracted_data.first_name, extracted_data.middle_name, extracted_data.last_name = separate_name(extracted_data.full_name)
        print(f"Extracted Data: {extracted_data}")

    # If the employee is not identified, we identify the employee based on the name or phone number.
    # If there are multiple employees with the same name, we pass in the error dict to the llm, this contains the email, number and name of all the matching employees.
    # These choices are then presented to the user to select the correct employee, this is done in the locate_update_employee function.
    if employee_id is None:

        # If the employee name is extracted, we need to find the best match for the employee name.
        if extracted_current_data.current_name and employee_identified == False:
            matched_name = find_best_match(user_input=extracted_current_data.current_name, choices=EmployeeChoices.get_all_employee_names(hr_company_id=employee_record.company_id, hr_group_id=employee_record.group_id), threshold=95)
            # Get the employee id by name.
            employee_name = EmployeeProxy.get_employee_id_by_name(
                name=matched_name,
                email=extracted_current_data.current_email,
                contact_number=extracted_current_data.current_phone_number,
                hr_group_id=employee_record.group_id,
                hr_company_id=employee_record.company_id
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
                
        # If the employee phone number is extracted, we identify the employee based on the phone number.
        if extracted_current_data.current_phone_number and employee_identified == False:
            employee_contact_result = EmployeeProxy.get_employee_id_by_contact(contact_number=extracted_current_data.current_phone_number, hr_group_id=employee_record.group_id, hr_company_id=employee_record.company_id)
            if employee_contact_result["success"] == False:
                print(f"Error: {employee_contact_result['error']}")
                error_dict = {employee_contact_result["error"]}
            else:
                employee_id = employee_contact_result["database_id"]
                employee_identified = True
                print(f"Employee Identified: {employee_id}")
                EmployeeSessionProxy.set_employee_identified(contact_number, True)
                EmployeeSessionProxy.set_employee_id(contact_number, employee_id)
               

    # Only attempt update if employee is identified and employee_id is valid
    if employee_identified and employee_id is not None:

        fields_mentioned = update_employee_fields_only(messages=session_messages[-2:])
        chosen_fields = [field for field in fields_mentioned.model_dump(exclude_none=True) if fields_mentioned.model_dump(exclude_none=True)[field]]
        print("fields with names:",chosen_fields)

        list_of_fields_with_no_value = [field for field in chosen_fields if field not in extracted_data.model_dump(exclude_none=True)]
        print(f"list_of_fields_to_update: {list_of_fields_with_no_value}")

        # We print the extracted fields and values, result, fields chosen by user, fields with value and error dict.
        print("--------------------------------")
        print(f"Extracted Fields and Values: {extracted_fields_and_values}")
        print(f"Update Result: {result}")
        print(f"Fields chosen by user: {chosen_fields}")
        print(f"Fields with value: {list_of_fields_with_no_value}")
        print("--------------------------------")


        # Checks if the user has mentioned any new information to update.
        if_fields_present = extracted_data.model_dump(exclude_none=True)
        print(f"If Fields Present: {if_fields_present}")

        # Get employee details for messages
        employee_details = EmployeeProxy.get_employee_record_by_id(employee_id)
        employee_name = employee_details.name if employee_details else "the employee"

        # Handle different scenarios based on what the user provided
        if if_fields_present and list_of_fields_with_no_value:
            # Scenario 1: User provided some fields with values AND some fields without values
            # Show confirmation for fields with values, ask for missing values
            
            # Add extracted fields and values to Redis for confirmation tracking
            for field, value in if_fields_present.items():
                EmployeeSessionProxy.add_field_to_confirmation_list(contact_number, field, str(value))
            
            # Format the fields with values for confirmation
            fields_display = []
            for field, value in if_fields_present.items():
                fields_display.append(f"• *{field}*: {value}")
            
            # Format the fields without values
            missing_fields = ", ".join(list_of_fields_with_no_value)
            
            confirmation_message = f"I can see you want to update *{employee_name}* with:\n\n" + "\n".join(fields_display)
            confirmation_message += f"\n\nPlease provide the updated values for these fields: {missing_fields}"
            
            # Don't set confirmation status yet - wait for missing values
            EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", confirmation_message)
            send_whatsapp_message(contact_number, confirmation_message)
            return
            
        elif if_fields_present and not list_of_fields_with_no_value:
            # Scenario 2: User provided fields with values, no missing values
            # Show confirmation message
            
            # Add extracted fields and values to Redis for confirmation tracking
            for field, value in if_fields_present.items():
                EmployeeSessionProxy.add_field_to_confirmation_list(contact_number, field, str(value))
            
            fields_display = []
            for field, value in if_fields_present.items():
                fields_display.append(f"• *{field}*: {value}")
            
            confirmation_message = f"Are you sure you want to make the following changes to *{employee_name}*?\n\n" + "\n".join(fields_display)
            
            # Set the update agent confirmation status to True
            EmployeeSessionProxy.set_update_agent_confirmation(contact_number, True)
            
            # Send the confirmation message
            EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", confirmation_message)
            send_whatsapp_message(contact_number, confirmation_message)
            return
            
        else:
            # Scenario 3 & 4: No fields with values provided OR no fields mentioned at all
            # Use the agent for these cases
            response = ask_user_what_else_to_update(extracted_fields_and_values, result, list_of_fields_with_no_value, fields_not_confirmed=extracted_not_confirmed)
            EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
            EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
            send_whatsapp_message(contact_number, response.message_to_user)
            return

    else:
        response = update_employee_response(messages=session_messages[-4:], employee_identified=employee_identified, error_dict=error_dict, fields=agent_states.mandatory_fields)
        EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
        EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
        send_whatsapp_message(contact_number, response.message_to_user)
        print(f"chat_assistant: {response}")


while True:
    user_input = input("User: ")
    update_employee_fields(contact_number="+971512345678", user_message=user_input)