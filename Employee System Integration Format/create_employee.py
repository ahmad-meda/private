from datetime import datetime, timedelta
from proxies.employee_message_proxy import EmployeeMessageHistoryProxy
from proxies.proxy import EmployeeProxy
from proxies.employee_session_proxy import EmployeeSessionProxy
from Utils.fields_to_add import agent_states
from Utils.current_field import remove_used_fields_and_return_next, remove_fields_by_name_and_return_next
from Utils.agents import ask_user_for_confirmation_to_add_employee, get_employee_details, extract_data, skipped_employee_details, ask_user_for_confirmation_to_clear_employee_draft, does_user_want_to_exit_add_employee
from Utils.fuzzy_logic import find_best_match
from Utils.choices import EmployeeChoices
from Utils.enum import DraftType
from Utils.sanitization import sanitize_messages
from Utils.name_separation import separate_name
from Utils.explanations import Explanations
from Utils.null_fields import get_null_fields
from Utils.dummy_functions import send_whatsapp_message, clear_session
from huse.backend import huse_update_employee_status, register_employee_in_huse
from huse.email import send_huse_credentials_email
from Utils.extraction_fields import get_filled_fields

def create_employee(contact_number:str, user_message:str):

    print("Entered Create Employee")

    # Boolean to regulate optional and mandatory fields.
    skip_optional_logic = False
    EmployeeMessageHistoryProxy.save_message(contact_number, "user", user_message)

     # Get the Sales Agent ID from thedatabase using the contact number
    agent_id, agent_name = EmployeeProxy.get_hr_id_by_contact(contact_number=contact_number)
    draft_table_id, draft_id, draft_existed = EmployeeProxy.get_draft(agent_id, DraftType.EMPLOYEE.value)
    EmployeeProxy._add_created_by_to_employee_record(employee_record_id=draft_id, hr_id=agent_id)

    # ------------------------ Main Logic STARTS Here --------------------------



    # Add the user message to the Redis session history - Refer to session service and proxy Files
    EmployeeSessionProxy.add_message(contact_number, {"role": "user", "content": user_message})


    # Get the previous messages of the conversation from the redis session history. 
    # We are using this because Postgres DB History isn't deleteable and may cause context confusion when a new conversation starts.
    extraction_messages = EmployeeSessionProxy.get_messages(contact_number)
    print(f"Extraction Messages: {extraction_messages}")

    does_user_want_to_exit = does_user_want_to_exit_add_employee(messages=extraction_messages)
    if does_user_want_to_exit.does_user_want_to_exit is True:
        EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", does_user_want_to_exit.message_to_user_on_exit)
        send_whatsapp_message(contact_number, does_user_want_to_exit.message_to_user_on_exit)
        EmployeeSessionProxy.clear_employee_session(contact_number)
        EmployeeSessionProxy.clear_messages(contact_number)
        clear_session(contact_number)
        return


    is_trying_to_add_new_employee = EmployeeSessionProxy.get_user_trying_to_add_new_employee(contact_number)
    print(f"Is trying to add new employee: {is_trying_to_add_new_employee}")

    asked_user_draft_continuation = EmployeeSessionProxy.get_asked_user_draft_continuation(contact_number)
    print(f"Asked user draft continuation: {asked_user_draft_continuation}")

    in_confirmation_stage = EmployeeSessionProxy.get_correcting_final_confirmation_changes(contact_number)
    print(f"Correcting final confirmation changes: {in_confirmation_stage}")

    record_to_check = EmployeeProxy.get_employee_draft_record_by_id(employee_id=draft_id)
    #check the time
    current_time = datetime.now()
    record_to_check_time = record_to_check.updated_at
    time_difference = current_time - record_to_check_time
    print(f"Time difference: {time_difference}")
    print(timedelta(minutes=30))
    
    # if the time is more than 30 minutes, then the user is trying to add a new employee
    # but only if we haven't just handled the draft confirmation
    if time_difference > timedelta(minutes=30) and not asked_user_draft_continuation:
        EmployeeSessionProxy.set_user_trying_to_add_new_employee(contact_number, True)

    if is_trying_to_add_new_employee:
        # Get proper names for ID fields using proxy methods
        company = EmployeeProxy.get_company_by_id(record_to_check.company_id)
        company_name = company.name if company else "None"
        
        role = EmployeeProxy.get_role_by_id(record_to_check.role_id)
        role_name = role.name if role else "None"
        
        office_location = EmployeeProxy.get_office_location_by_id(record_to_check.office_location_id)
        office_location_name = office_location.name if office_location else "None"
        
        department = EmployeeProxy.get_department_by_id(record_to_check.department_id)
        department_name = department.name if department else "None"
        
        reporting_manager = EmployeeProxy.get_reporting_manager_by_id(record_to_check.reporting_manager_id)
        reporting_manager_name = reporting_manager.name if reporting_manager else "None"
        
        draft_continuation_message = f"You already have a draft with an employee's details, are you sure you want to continue with the draft or add a new employee?\n Here are the employee details:\n\n*Full Name*: {record_to_check.name}\n*Contact Number*: +{record_to_check.contact_no}\n*Email*: {record_to_check.email_id}\n*Company*: {company_name}\n*Role*: {role_name}\n*Office Location*: {office_location_name}\n*Department*: {department_name}\n*Reporting Manager*: {reporting_manager_name}\n*Designation*: {record_to_check.designation}\n*Date Of Joining*: {record_to_check.date_of_joining}\n*Date Of Birth*: {record_to_check.date_of_birth}\n*Gender*: {record_to_check.gender}\n*Reminders*: {record_to_check.reminders}\n*Is HR*: {record_to_check.is_hr}\n*HR Scope*: {record_to_check.hr_scope}\n*Home Latitude*: {record_to_check.home_latitude}\n*Home Longitude*: {record_to_check.home_longitude}"
        send_whatsapp_message(contact_number, draft_continuation_message)
        EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", draft_continuation_message)
        EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": draft_continuation_message})
        EmployeeSessionProxy.set_asked_user_draft_continuation(contact_number, True)
        EmployeeSessionProxy.set_user_trying_to_add_new_employee(contact_number, False)
        return
    

    if asked_user_draft_continuation is True:
        draft_continuation_result = ask_user_for_confirmation_to_clear_employee_draft(messages=extraction_messages[-2:])
        if draft_continuation_result.does_user_want_to_clear_the_draft is True:
            EmployeeProxy.clear_employee_draft_fields(draft_id=draft_id)
            EmployeeSessionProxy.set_user_trying_to_add_new_employee(contact_number, False)
            EmployeeSessionProxy.set_asked_user_draft_continuation(contact_number, False)
        else:
            if draft_continuation_result.is_user_intent_clear == True:
                send_whatsapp_message(contact_number, draft_continuation_result.message_when_intent_not_clear)
                EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", draft_continuation_result.message_when_intent_not_clear)
                EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": draft_continuation_result.message_when_intent_not_clear})
                EmployeeSessionProxy.set_user_trying_to_add_new_employee(contact_number, False)
                EmployeeSessionProxy.set_asked_user_draft_continuation(contact_number, False)
                return
            else:
                EmployeeSessionProxy.set_user_trying_to_add_new_employee(contact_number, False)
                EmployeeSessionProxy.set_asked_user_draft_continuation(contact_number, False)
                
            


    # Get all the null fields from the employee record
    main_fields, optional_personal_fields, optional_employment_fields, optional_location_fields = get_null_fields(draft_id)
    # Im storing all the fields that have default values when a record is created over here, if the user answers this fields or skips it, then its added to the redis session list. the fields in this list arent asked again.
    session_fields = EmployeeSessionProxy.get_list(contact_number=contact_number)
    print(f"Session Fields: {session_fields}")
    
    # Check if the company is in null fields, if its not then also check if the its session fields, if not then check the office location registered to thst company
    if "company_name" not in main_fields and "company_name" not in session_fields:
        #get the company from the db and then if it has any office location
        draft_record_company = EmployeeProxy.get_employee_draft_record_by_id(employee_id=draft_id)
        if draft_record_company.company_id is not None:
            avaliable_office_locations = EmployeeProxy.get_office_locations_by_group_and_company(group_id=draft_record_company.group_id, company_id=draft_record_company.company_id)
            if avaliable_office_locations is []:
                EmployeeSessionProxy.add_to_list(contact_number=contact_number, items=["office_location_name"])
            
    
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
    

    # Auto-assign company when user has no group, after adding the company remove it from the main_fields list, so that it wont be asked.
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
    # Explanations are passed to the LLM besides the fields so the LLM knows what each field means and so that it can explain to the user. 
    error_dict = {}
    explanations = {}  # Clear explanations at the start of each iteration
    asked_confirmation = EmployeeSessionProxy.get_employee_asked_confirmation(contact_number=contact_number) # Get the asked confirmation status for the employee       

    multiple_office_locations_result = EmployeeSessionProxy.get_multiple_office_locations(contact_number=contact_number)
    print(f"Multiple Office Locations Result: {multiple_office_locations_result}")

#------------------------------------------------------------------------------------------------------------------------------------   
    if asked_confirmation == True:
        llm_response = ask_user_for_confirmation_to_add_employee(messages=extraction_messages[-2:])
        print(f"LLM Response: {llm_response}")
        if llm_response.does_user_want_to_add_the_employee == True:
            print("Adding in main database")
            add_result = EmployeeProxy._add_employee_in_main_database(draft_id=draft_id)
            print(f"adding in main database: ", add_result)

            if "error" in add_result:
                print(f"ERROR: Failed to add employee to main database: {add_result['error']}")
                # Send error message to user
                error_message = f"Sorry, there was an error adding the employee to the database: {add_result['error']}. Please try again or contact support."
                EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", error_message)
                send_whatsapp_message(contact_number, error_message)
                return
            
            # Create leave balances for the newly created employee
            if "new_employee_id" in add_result:
                
                print("Clearing messages")
                EmployeeSessionProxy.clear_messages(contact_number=contact_number) # clear the redis message history after the employee has been successfully added
                print(f"Messages: {EmployeeSessionProxy.get_messages(contact_number=contact_number)}")

                new_employee_id = add_result["new_employee_id"]
                print(f"Creating leave balances for employee ID: {new_employee_id}")
                leave_balance_result = EmployeeProxy.create_leave_balances_for_employee(employee_id=new_employee_id)
                print(f"Leave balance creation result: {leave_balance_result}")

                office_location_ids = EmployeeSessionProxy.get_multiple_office_locations(contact_number=contact_number)
                if office_location_ids != []:
                    EmployeeProxy.save_office_locations_to_employee(employee_id=new_employee_id, office_location_ids=office_location_ids)

                # Create account username and password for the new employee
                employee_obj = EmployeeProxy.get_employee_record_by_id(new_employee_id)
                employee_data = {
                                'id': employee_obj.id,
                                'name': employee_obj.name,
                                'emailId': employee_obj.emailId,
                                'contactNo': "+" + employee_obj.contactNo,
                                'gender': employee_obj.gender,
                                'designation': employee_obj.designation,
                                'dateOfJoining': employee_obj.dateOfJoining,
                                'dateOfBirth': employee_obj.dateOfBirth,
                                'first_name': employee_obj.first_name,
                                'middle_name': employee_obj.middle_name,
                                'last_name': employee_obj.last_name
                            }
                print(f"Employee data: {employee_data}")
                # Register Employee in HUSE - Create User Account API is being used here.
                result = register_employee_in_huse(employee_data)

                # After Registering the Employee, send the user his credentials. The HR is also sent the credentials.
                if result and result.get('success'):
                    # Extract credentials from the response
                    credentials = result.get('credentials', {})
                    huse_data = result.get('data', {})
                    
                    # Debug: Print what we're sending to email function
                    print("Email parameters:")
                    print(f"employee_email: {employee_data.get('emailId')}")
                    print(f"username: {credentials.get('username')}")
                    print(f"password: {credentials.get('password')}")
                    print(f"security_question: {huse_data.get('securityQuestion')}")
                    print(f"security_answer: {result.get('security_answer')}")
                    
                    # Validate email sending parameters
                    if not employee_data.get('name') or not employee_data.get('emailId'):
                        print("Error: Missing employee name or email")
                        return {"success": False, "message": "Missing employee name or email"}
                    
                    if not credentials.get('username') or not credentials.get('password'):
                        print("Error: Missing credentials")
                        return {"success": False, "message": "Missing credentials"}
                    
                    try:
                        response = send_huse_credentials_email(
                            employee=employee_data.get('name'),
                            employee_emails=[employee_data.get('emailId')],
                            username=credentials.get('username'),
                            password=credentials.get('password'),
                            security_question=huse_data.get('securityQuestion'),
                            security_answer=result.get('security_answer')  # Use locally generated security answer
                        )
                    except Exception as e:
                        print(f"Error: Failed to send credentials email - {str(e)}")
                        return {"success": False, "message": f"Failed to send credentials email: {str(e)}"}
                    
                    # Change the status of the account created for the employee to active - "3" is the status for active accounts.
                    huse_user_id = result.get('data', {}).get('id')
                    if huse_user_id:
                        try:
                            status_result = huse_update_employee_status(user_id=huse_user_id, status=3)
                            print(f"Status update result: {status_result}")
                        except Exception as e:
                            print(f"Error: Failed to update employee status - {str(e)}")
                            return {"success": False, "message": f"Failed to update employee status: {str(e)}"}
                else:
                    print(f"Failed to register employee: {result}")
                                    
            EmployeeMessageHistoryProxy.clear_message_history(contact_number)
            EmployeeSessionProxy.clear_list(contact_number=contact_number) # clear the redis message history after the employee has been successfully added
            EmployeeSessionProxy.clear_messages(contact_number=contact_number) # clear the redis message history after the employee has been successfully added
            EmployeeSessionProxy.clear_multiple_office_locations(contact_number=contact_number) # clear the multiple office locations after the employee has been successfully added
            EmployeeSessionProxy.clear_employee_asked_confirmation(contact_number=contact_number)
            EmployeeSessionProxy.clear_correcting_final_confirmation_changes(contact_number=contact_number)
            #Get the new employee Record
            added_employee = EmployeeProxy.get_employee_draft_record_by_id(employee_id=draft_id)
            end_message = f"Employee {added_employee.name} has been successfully added to the database!"
            EmployeeProxy._delete_draft(draft_id=draft_table_id)
            send_whatsapp_message(contact_number, end_message)
            clear_session(contact_number)
            print(" --------------------- MESSAGES CLEARED --------------------- ")
            print(" --------------------- SESSION CLEARED --------------------- ")
            print(" --------------------- CONFIRMATION VARIABLE CLEARED --------------------- ")
            print(" --------------------- EMPLOYEE ID CLEARED --------------------- ")
            return
            
        elif llm_response.does_user_want_to_add_the_employee == False:
            if llm_response.did_user_mention_editing_employee_details:
                EmployeeSessionProxy.set_employee_asked_confirmation(contact_number, False)
                EmployeeSessionProxy.set_correcting_final_confirmation_changes(contact_number, True)
                pass
            else:
                send_whatsapp_message(contact_number, llm_response.farewell_message_to_user)
                EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", llm_response.farewell_message_to_user)
                EmployeeSessionProxy.clear_messages(contact_number)
                EmployeeSessionProxy.clear_employee_asked_confirmation(contact_number)
                EmployeeSessionProxy.clear_employee_session(contact_number)
                EmployeeSessionProxy.clear_correcting_final_confirmation_changes(contact_number)
                clear_session(contact_number)
                print(" --------------------- MESSAGES CLEARED --------------------- ")
                print(" --------------------- SESSION CLEARED --------------------- ")
                print(" --------------------- CONFIRMATION VARIABLE CLEARED --------------------- ")
                print(" --------------------- EMPLOYEE ID CLEARED --------------------- ")
                return


    # Last 2 messages from session history are passed to the LLM Extraction Agent. 
    # Passing too many previous messages may cause the extraction of a single/multiple field/s to occur in multiple iterations.
    
    # Create dictionary of filled fields from draft record (reusing record_to_check from above)
    # Get names from IDs when they exist
    filled_fields = get_filled_fields(record_to_check=record_to_check)
    print(f"Filled Fields: {filled_fields}")
    extracted_data = extract_data(messages=extraction_messages[-2:], list_of_fields=filled_fields)
    print(f"Extracted Data: {extracted_data}")


    # This is Fuzzy Logic, best way to explain - if you have a type, fuzzy logic corrects it.
    # If there isnt a match at all based on the users input, it returns the user choice itself.
    # This is so it gets passed to service function where an error is raised and recorded in the error dictionary, which is then passed to the LLM to inform the user regarding the issue.
    if extracted_data.full_name or extracted_data.work_policy_name or extracted_data.office_location_name or extracted_data.department_name or extracted_data.reporting_manager_name or extracted_data.role or extracted_data.company_name or extracted_data.gender :
        extracted_data.work_policy_name = find_best_match(user_input=extracted_data.work_policy_name, choices=EmployeeChoices.get_work_policy_choices(), threshold=95)
        extracted_data.office_location_name = find_best_match(user_input=extracted_data.office_location_name, choices=EmployeeChoices.get_office_location_choices(group_id=employee_record.group_id, company_id=employee_record.company_id), threshold=95)
        extracted_data.department_name = find_best_match(user_input=extracted_data.department_name, choices=EmployeeChoices.get_departments_choices(), threshold=95)
        extracted_data.reporting_manager_name = find_best_match(user_input=extracted_data.reporting_manager_name, choices=EmployeeChoices.get_reporting_manager_choices(hr_company_id=employee_record.company_id, hr_group_id=employee_record.group_id), threshold=95)
        extracted_data.role = find_best_match(user_input=extracted_data.role, choices=EmployeeChoices.get_role_choices(), threshold=95)
        extracted_data.company_name = find_best_match(user_input=extracted_data.company_name, choices=EmployeeChoices.get_companies_choices(group_id=employee_record.group_id, company_id=employee_record.company_id), threshold=95)
        extracted_data.gender = find_best_match(user_input=extracted_data.gender, choices=EmployeeChoices.get_gender_choices(), threshold=95)

        # No Fuzzy logic here, just manually splitting name into first, middle and last, sometimes the llm can be a pain.
        extracted_data.first_name, extracted_data.middle_name, extracted_data.last_name = separate_name(extracted_data.full_name)
    
    # I'm only running the service function when a field value has been extracted, this is in place so that unecessary db calls can be avoided.
    print("If any data has been extracted from the user message",extracted_data.model_dump(exclude_none=True))
    # Only run db service function if something has been extracted from the user message
    given_fields = extracted_data.model_dump(exclude_none=True)
    print(f"Given Fields: {given_fields}")

    if in_confirmation_stage != True:
        if any(field in given_fields for field in ["full_name", "contact_number", "emailId"]):

            print("in all if loop")
            print("record_to_check.name", record_to_check.name)
            print("record_to_check.contact_no", record_to_check.contact_no)
            print("record_to_check.email_id", record_to_check.email_id)

            if record_to_check.name != None and "full_name" in given_fields:
                EmployeeSessionProxy.set_user_trying_to_add_new_employee(contact_number, True)
                print("changing")
            elif record_to_check.contact_no != None and "contact_number" in given_fields:
                EmployeeSessionProxy.set_user_trying_to_add_new_employee(contact_number, True)
            elif record_to_check.email_id != None and "emailId" in given_fields:
                EmployeeSessionProxy.set_user_trying_to_add_new_employee(contact_number, True)

            is_trying_to_add_new_employee = EmployeeSessionProxy.get_user_trying_to_add_new_employee(contact_number)
            print(f"Is trying to add new employee: {is_trying_to_add_new_employee}")

    if is_trying_to_add_new_employee:
        # Get proper names for ID fields using proxy methods
        company = EmployeeProxy.get_company_by_id(record_to_check.company_id)
        company_name = company.name if company else "None"
        
        role = EmployeeProxy.get_role_by_id(record_to_check.role_id)
        role_name = role.name if role else "None"
        
        office_location = EmployeeProxy.get_office_location_by_id(record_to_check.office_location_id)
        office_location_name = office_location.name if office_location else "None"
        
        department = EmployeeProxy.get_department_by_id(record_to_check.department_id)
        department_name = department.name if department else "None"
        
        reporting_manager = EmployeeProxy.get_reporting_manager_by_id(record_to_check.reporting_manager_id)
        reporting_manager_name = reporting_manager.name if reporting_manager else "None"
        
        draft_continuation_message = f"You already have a draft with an employee's details, are you sure you want to continue with the draft or add a new employee?\n Here are the employee details:\n\n*Full Name*: {record_to_check.name}\n*Contact Number*: +{record_to_check.contact_no}\n*Email*: {record_to_check.email_id}\n*Company*: {company_name}\n*Role*: {role_name}\n*Office Location*: {office_location_name}\n*Department*: {department_name}\n*Reporting Manager*: {reporting_manager_name}\n*Designation*: {record_to_check.designation}\n*Date Of Joining*: {record_to_check.date_of_joining}\n*Date Of Birth*: {record_to_check.date_of_birth}\n*Gender*: {record_to_check.gender}\n*Reminders*: {record_to_check.reminders}\n*Is HR*: {record_to_check.is_hr}\n*HR Scope*: {record_to_check.hr_scope}\n*Home Latitude*: {record_to_check.home_latitude}\n*Home Longitude*: {record_to_check.home_longitude}"
        send_whatsapp_message(contact_number, draft_continuation_message)
        EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", draft_continuation_message)
        EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": draft_continuation_message})
        EmployeeSessionProxy.set_asked_user_draft_continuation(contact_number, True)
        EmployeeSessionProxy.set_user_trying_to_add_new_employee(contact_number, False)
        return


    # Only run db service function if something has been extracted from the user message
    if given_fields:
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
            multiple_office_locations_result = EmployeeProxy.save_employee_office_locations(employee_id=draft_id, office_location_names=corrected_location_names)
            error_dict = multiple_office_locations_result['errors']

            # Save the office location IDs to Redis session
            EmployeeSessionProxy.set_multiple_office_locations(contact_number=contact_number, location_names=multiple_office_locations_result["office_location_ids"])
    
        
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
    if current_field is None and error_dict != {}:
        response = get_employee_details(messages=extraction_messages, fields=remaining_fields, error_dict=error_dict, explanations=explanations)
        EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
        EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
        print(f"Assistant: {response.message_to_user}")
        send_whatsapp_message(contact_number, response.message_to_user)
        return
        
    # If there are no fields left to add and there are no errors to report then end the add employee agent interaction.
    if current_field is None and len(remaining_fields) == 0 and error_dict == {}:
        draft_employee_id = EmployeeProxy.get_employee_draft_record_by_id(employee_id=draft_id)
        # Get proper names for ID fields using proxy methods
        company = EmployeeProxy.get_company_by_id(draft_employee_id.company_id)
        company_name = company.name if company else "None"
        
        role = EmployeeProxy.get_role_by_id(draft_employee_id.role_id)
        role_name = role.name if role else "None"
        
        office_location = EmployeeProxy.get_office_location_by_id(draft_employee_id.office_location_id)
        office_location_name = office_location.name if office_location else "None"
        
        department = EmployeeProxy.get_department_by_id(draft_employee_id.department_id)
        department_name = department.name if department else "None"
        
        reporting_manager = EmployeeProxy.get_reporting_manager_by_id(draft_employee_id.reporting_manager_id)
        reporting_manager_name = reporting_manager.name if reporting_manager else "None"
        
        message = f"Alright! Before we add the employee, pls confirm if all the details are correct:\n*Full Name*: {draft_employee_id.name}\n*Contact Number*: +{draft_employee_id.contact_no}\n*Email*: {draft_employee_id.email_id}\n*Company*: {company_name}\n*Role*: {role_name}\n*Office Location*: {office_location_name}\n*Department*: {department_name}\n*Reporting Manager*: {reporting_manager_name}\n*Designation*: {draft_employee_id.designation}\n*Date Of Joining*: {draft_employee_id.date_of_joining}\n*Date Of Birth*: {draft_employee_id.date_of_birth}\n*Gender*: {draft_employee_id.gender}\n*Reminders*: {draft_employee_id.reminders}\n*Is HR*: {draft_employee_id.is_hr}\n*HR Scope*: {draft_employee_id.hr_scope}\n*Home Latitude*: {draft_employee_id.home_latitude}\n*Home Longitude*: {draft_employee_id.home_longitude}"
        send_whatsapp_message(contact_number, message)
        EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", message)
        EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": message})
        EmployeeSessionProxy.set_employee_asked_confirmation(contact_number=contact_number, asked_confirmation=True)
        EmployeeSessionProxy.set_user_trying_to_add_new_employee(contact_number, False)
        return
    # When the user first tries to add an employee, after the first message, we display all the fields and what they require to add an employee.
    # All the fields are listed and an example of what the field value should be is also given.
    # Additionally, certain fields explanations are passed as well to make sure the LLM doesn't hallucinate.
    if draft_existed is False:
    
        # place all fields here, this is to show the user what all details are needed to add an employee
        remaining_fields = ["full_name", "contact_number", "company_name", "role", "office_location_name", "department_name", "reporting_manager_name", "emailId", "designation", "dateOfJoining", "dateOfBirth", "gender", "reminders", "is_hr", "hr_scope"]
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
        office_list = EmployeeProxy.get_office_locations_by_group_and_company(group_id=employee_record.group_id, company_id=employee_record.company_id)
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
    send_whatsapp_message(contact_number, response.message_to_user)
    EmployeeSessionProxy.add_message(contact_number, {"role": "assistant", "content": response.message_to_user})
    EmployeeMessageHistoryProxy.save_message(contact_number, "assistant", response.message_to_user)
    print(f"Assistant: {response.message_to_user}")

        
while True:
    user_input = input("User: ")
    create_employee(contact_number="+971512345678", user_message=user_input)

       


        