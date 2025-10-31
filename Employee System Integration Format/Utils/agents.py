from Utils.formats import AskUserForConfirmationToUpdateEmployee, EmployeeAgent, SoftDeleteEmployeeResponse, SoftDeleteExtraction, UpdateEmployeeResponse, UpdateEmployeeExtraction, SkippedDetails, LocateUpdateEmployeeResponse, get_employee_values, get_employee_chat_message, UpdateEmployeeEndResponse, AskUserWhatElseToUpdate, EmployeeUpdateFields, AskUserForConfirmation, AskUserForConfirmationToAddEmployee, AskUserForConfirmationToClearEmployeeDraft, IntentToExitEmployee       
from Utils.ai_client import client
from Files.SQLAlchemyModels import Employee
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal

model = "gpt-4o"

def get_employee_details(messages:list, fields:list, error_dict:dict, explanations:dict):

    system_message = [  
        {
            "role": "system",
            "content": (
            #     f"""You are a warm, friendly HR assistant, who is helping a HR agent to add an employee by asking these {fields}. 
            #         Based on the {fields} and {error_dict}, your ONLY job is to create a reply to the user BY ALWAYS asking about these missing {fields} in one go and {error_dict}. 
            #         explain what they mean only using this : {explanations}.

            #         Its a whatsapp chat, so responses have to be casual and friendly.
            #         Always refer to the employee in the third person, even if the HR agent uses first-person language. Do not assume the details being shared are about the HR themselves."""
            # 
            f""" You are a warm, friendly HR assistant asking a HR agent for Employee details in whatsapp chat to add an employee.

                    Create a casual, human, WhatsApp reply to the HR agent who doesnt know the backend using:
                    The following fields are missing or incorrect: {fields} and inform them of the errors: {error_dict}.
                    some fields require explanantion: {explanations}.
                    
                    - Always refer to the employee in third person, even if the HR agent uses first-person language.
                    Keep it very direct, no emoji, short and easy to read and friendly.
                    ask all the fields in one go"""
            )
        }
    ]
        
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=EmployeeAgent
    )

    return completion.choices[0].message.parsed

def extract_data(messages, list_of_fields: dict, company_choices:list, role_choices:list, department_choices:list, gender_choices:list, office_location_choices:list):

    class EmployeeData(BaseModel):
        employee_id: Optional[str] = Field(description="This is the employee id of the employee to be added. Extract this if the user gives a employee id.")
        full_name: Optional[str] = Field(description="This is the name of the employee to be added. Extract this if the user gives a first name or first and last name or first last and middle name.")
        contact_number: Optional[str] = Field(description="This is the contact number of the employee to be added. Extract this if the user gives a contact number.")
        first_name: Optional[str] = Field(description="This is the first name of the employee to be added. Extract this if the user gives a first name.")
        last_name: Optional[str] = Field(description="This is the last name of the employee to be added. Extract this if the user gives a last name.")
        middle_name: Optional[str] = Field(description="This is the middle name of the employee to be added. Extract this if the user gives a middle name.")
        emailId: Optional[str] = Field(description="This is the email of the employee to be added. Extract this if the user gives an email.")
        designation: Optional[str] = Field(description="This is the designation of the employee to be added. Extract this if the user gives a designation.")
        dateOfJoining: Optional[str] = Field(description="This is the date of joining of the employee to be added. Extract this if the user gives a date of joining.")
        dateOfBirth: Optional[str] = Field(description="This is the date of birth of the employee to be added. Extract this if the user gives a date of birth.")
        gender: Optional[str] = Field(description=f"This is the gender of the employee to be added, can be Male or Female. Extract this if the user gives a gender.Here are the choices of the gender: {gender_choices}")
        work_policy_name: Optional[str] = Field(description="This is the work policy of the employee to be added. Extract this if the user gives a work policy.")
        home_latitude: Optional[float] = Field(description="This is the home latitude of the employee to be added. Extract this if the user gives a home latitude.")
        home_longitude: Optional[float] = Field(description="This is the home longitude of the employee to be added. Extract this if the user gives a home longitude.")
        office_location_name: Optional[str] = Field(description=f"The user can either provide the name of office location or provide the home coordinates(if they choose this then extract the office location as 'home_coordinates') or may refuse to give the office location (this is a privilege only for managers), so if they choose the manager-skip extract the office location as 'manager_skip'. Here are the choices of the office locations: {office_location_choices}")
        company_name: Optional[str] = Field(description=f"This is the company of the employee to be added. Extract this if the user gives a company.Here are the choices of the companies: {company_choices}")
        role: Optional[str] = Field(description=f"This is the role of the employee to be added. Extract this if the user gives a role.Here are the choices of the roles: {role_choices}")
        reporting_manager_name: Optional[str] = Field(description="This is the reporting manager of the employee to be added. Extract this if the user gives a reporting manager.")
        department_name: Optional[str] = Field(description=f"This is the department of the employee to be added. Extract this if the user gives a department.Here are the choices of the departments: {department_choices}")
        restrict_to_allowed_locations: Optional[bool] = Field(description="This is True if the user wants multiple office locations for the employee.")
        allow_site_checkin: Optional[bool] = Field(description="This is True if the employee is allowed to check-in from any location otherwise False.")
        reminders: Optional[bool] = Field(description="This is True if the employee wants reminders for check-in and check-out. Extract this if the user gives a reminder.")
        is_hr: Optional[bool] = Field(description="This is True if the employee being added is an HR.")
        hr_scope: Optional[str] = Field(description="This is the scope of the HR. It can be 'company' or 'group'. Extract this if the user gives a scope.")
        multiple_office_locations_to_check_in: Optional[List[str]] = Field(description="This is a list of office locations to check-in from. The bot will ask the user the multiple office locations for the employee to checkin from. The user will give names of the office locations to check-in from.")


    extraction_messages = [
        {
            "role": "system",
            "content": (

                f"""You are a data extraction assistant. Extract the confirmed employee info as structured data
                
                CURRENT DRAFT RECORD Collected Data 
                {list_of_fields}

                From this conversation, only extract the fields that are empty and the fields that are provided by the user.
                
                VERY IMPORTANT: Only extract NEW information that the user is providing in their current message. Never hallucinate.
                Date format: YYYY-MM-DD
                Name format: Professional case (First Last)
                """
            )
        }
    ] + messages

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=extraction_messages,
        response_format=EmployeeData,
    )
    return completion.choices[0].message.parsed


def skipped_employee_details(messages, fields: list):
            skipped_messages = [
                {
                    "role": "system",
                    "content": (
                        f"""You are analyzing which fields the user doesnt want to answer by his intent.
                        the user is presented with these fields: {fields}.
                        the skipped fields should include the fields that the user doesnt want to answer by his intent.
                        look at the agents question's and the user's response to it and decide which fields the user doesnt want to answer by his intent.
                        only mention the fields that he want to skip in the skipped_fields list.
                                                                        """
                    )
                }
            ] + messages

            completion = client.beta.chat.completions.parse(
                model=model,
                messages=skipped_messages,
                response_format=SkippedDetails,
            )
            return completion.choices[0].message.parsed

def soft_delete_employee_response(messages:list, fields:list, error_dict:dict):

    system_message = [
        {
            "role": "system",
            "content": (
                f"""You are a warm, friendly HR assistant for deleting employee, who is chatting with an HR agent to delete an employee only with  {fields} and {error_dict}. 
                    Based strictly on the {fields} and {error_dict}, your only job is to create a reply to the user by always asking them about the missing {fields} and 
                    tell them about the error: {error_dict}. 

                    The user can only be identified by their phone number OR name(Any one of these is enough). no other fields of the employee can be used to identify the employee.

                    Always refer to the employee in the third person, even if the HR agent uses first-person language. Do not assume the details being shared are about the HR themselves.
                    the error is for you to understand and inform the user as a human would. dont display the error to them.
                    
                    Look at the error and the fields and formulate a natural human like whatsapp response to the user. Always use plain english without code words."""
            )
        }
    ]
    
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=SoftDeleteEmployeeResponse
    )
    return completion.choices[0].message.parsed

def soft_delete_employee_extraction(messages:list):

    system_message = [
        {
            "role": "system",
            "content": (
                    """You are a data extraction assistant used for extracting the employee exiting details so that his record can be soft deleted. Extract details from the conversation between the user and the bot. end goal is to extract all present details of the employee that needs to be deleted.
                    """
            )
        }
    ] + messages

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=SoftDeleteExtraction
    )

    return completion.choices[0].message.parsed

def update_employee_extraction(messages:list):

    system_message = [
        {
            "role": "system",
            "content": (
                    """You are a data extraction assistant being used to update an employee in the db. 
                    You are supposed to extract only the NEW data the user wants to update.Do not extract the data the user has provided to identify the employee.
                    From this conversation, extract the confirmed employee new details as structured data. Never hallucinate.
                    
                    FIELD HANDLING:
                    - full_name: Complete employee name as provided
                    - first_name: First name of the employee
                    - middle_name: Middle name of the employee
                    - last_name: Last name of the employee
                    - contact_number: Phone number with country code if provided
                    - company_name: Name of the company/organization
                    - emailId: Complete email address
                    - dateOfBirth: Date of birth in postgres format (YYYY-MM-DD)
                    - gender: Gender as specified (Male or Female)
                    - designation: Job title or position
                    - dateOfJoining: Employment start date in postgres format (YYYY-MM-DD)
                    - role: Work role or function
                    - reporting_manager_name: Name of direct supervisor/manager
                    - department_name: Department or division name
                    - work_policy_name: Work policy type (remote, hybrid, on-site, etc.)
                    - office_location_name: Name of office location/branch
                    - home_latitude: Latitude coordinate of home address (as float)
                    - home_longitude: Longitude coordinate of home address (as float)
                    - restrict_to_allowed_locations: Boolean - True if user wants multiple office locations
                    - allow_site_checkin: Boolean - True if employee can check-in from any location
                    - reminders: Boolean - True if employee wants check-in/check-out reminders
                    - is_hr: Boolean - True if employee is HR
                    - hr_scope: String - HR scope can be 'company' or 'group'
                    
                    FORMATTING RULES:
                    - Dates in postgres format (YYYY-MM-DD)
                    - Names in professional format (upper and lower case)
                    - Extract only fields that the user explicitly wants to update. Never hallucinate.
                    """
            )
        }
    ] + messages

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=UpdateEmployeeExtraction,
        temperature=0.1
    )

    return completion.choices[0].message.parsed
      
def update_employee_response(messages:list, employee_identified:bool, error_dict:dict, fields:list):

    system_message = [
        {
            "role": "system",
            "content": (
                f"""
                    You are a warm, fiendly HR Assisstant, who is helping the HR to update a employee details in a whatsapp chat.
                    Has the employee been identified: {employee_identified }
                    Also inform the error_dict in plain english without coding syntax to the user when locating the employee: {error_dict}
                    If user identified is False then ask the user to give any one of these fields to locate the employee: {fields}. One of these fields is enough to locate the employee.

                    If employee identified is "True" DO NOT  mention anything about fields to locate the employee. Ask the HR what he/she wants to update and the new value of that field.
                    Always refer to the employee in the third person, even if the HR agent uses first-person language. Do not assume the details being shared are about the HR themselves.
"""
            )
        }
    ] + messages
    
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=UpdateEmployeeResponse
    )
    return completion.choices[0].message.parsed

def locate_update_employee(messages:list):

    system_message = [
        {
            "role": "system",
            "content": (
                """ You are a data extraction assistant used for extracting the employee existing details name or phone number so that his details can be updated.
                """
            )
        }
    ] + messages

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=LocateUpdateEmployeeResponse
    )
    return completion.choices[0].message.parsed
    
def get_employee_search_extraction(messages: list, employee_record: Employee):
    
    system_message = [
        {
            "role": "system",
            "content": (
                f"""
                You are an expert in extracting employee search criteria from user messages.

                these are the details of the employee chatting with you: {employee_record.contactNo}, and the name: {employee_record.name}
                
                TASK: Extract employee search information from user messages and return them as a structured search object.
                
                DATA STRUCTURE:
                - fields: List[get_employee_fields] - a list of search field objects
                - all_fields_given: bool - whether all required information has been provided
                - message_to_user: str - message to display to user if more information is needed
                - Each get_employee_fields object has: {{"fields": List[db_employee_fields], "field_name": str, "field_value": str}}
                
                AVAILABLE FIELD NAMES (from db_employee_fields):
                - employeeId, name, emailId, designation, dateOfJoining, dateOfBirth
                - contactNo, gender, office_location_name, work_policy_name
                - home_latitude, home_longitude, company_name, group_name
                - reporting_manager_name, role_name, department_name, checked_in, checked_out
                
                INSTRUCTIONS:
                1. Extract search criteria from the ENTIRE conversation history
                2. Look through ALL messages for employee search criteria
                3. Extract field-value pairs for searching employees
                4. Use exact values provided by the user
                5. When multiple employee names are mentioned, create separate entries for each name
                6. Map user queries to appropriate database field names:
                   - "engineering employees" → field_name: "department_name", field_value: "Engineering"
                   - "TechCorp workers" → field_name: "company_name", field_value: "TechCorp"
                   - "Dubai office" → field_name: "office_location_name", field_value: "Dubai"
                   - "John's team members" → field_name: "reporting_manager_name", field_value: "John"
                   - "female employees" → field_name: "gender", field_value: "female"
                   - "Ahmad Meda" → field_name: "name", field_value: "Ahmad Meda"
                   - "CEO" → field_name: "designation", field_value: "CEO"
                   - "john@company.com" → field_name: "emailId", field_value: "john@company.com"
                   - "my details", "my profile", "show me my details", "what is my email", "my role", "my department", "my company", "my manager" → field_name: "contactNo", field_value: [use the contact_number parameter provided above]
                7. For missing information, set all_fields_given to false and provide helpful message_to_user
                8. Once all required search criteria are provided, set all_fields_given to true
                9. IMPORTANT: If user provides ANY valid field-value pair (like a name, email, department, etc.), set all_fields_given to true as this is sufficient to perform a search
                10. Only set all_fields_given to false when the user's request is too vague or provides no searchable criteria
                11. Be thorough - check every message for search details
                12. Remember: A single valid search criterion (name, email, department, etc.) is sufficient for a search - set all_fields_given to true in such cases
                13. SELF-REFERENCE: When user asks about themselves ("my details", "my info", "my profile", etc.), automatically use the contact number from the employee_record parameter to search for their own information
                
                EXAMPLES:
                Input: "show me engineering employees"
                Output: {{"fields": [{{"field_name": "department_name", "field_value": "Engineering"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "find TechCorp workers"
                Output: {{"fields": [{{"field_name": "company_name", "field_value": "TechCorp"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "who works in Dubai office?"
                Output: {{"fields": [{{"field_name": "office_location_name", "field_value": "Dubai"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "list John's team members"
                Output: {{"fields": [{{"field_name": "reporting_manager_name", "field_value": "John"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "show all female employees"
                Output: {{"fields": [{{"field_name": "gender", "field_value": "female"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "the name is Ahmad Meda"
                Output: {{"fields": [{{"field_name": "name", "field_value": "Ahmad Meda"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "I want info on Ahmad, Ali and Meda"
                Output: {{"fields": [{{"field_name": "name", "field_value": "Ahmad"}}, {{"field_name": "name", "field_value": "Ali"}}, {{"field_name": "name", "field_value": "Meda"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "show me employees with CEO designation in Dubai office"
                Output: {{"fields": [{{"field_name": "designation", "field_value": "CEO"}}, {{"field_name": "office_location_name", "field_value": "Dubai"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "find employees born in 1990"
                Output: {{"fields": [{{"field_name": "dateOfBirth", "field_value": "1990"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "search for john@company.com"
                Output: {{"fields": [{{"field_name": "emailId", "field_value": "john@company.com"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "show employees who joined in 2023"
                Output: {{"fields": [{{"field_name": "dateOfJoining", "field_value": "2023"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "hi, pls give me contact number for Ahmad Meda"
                Output: {{"fields": [{{"field_name": "name", "field_value": "Ahmad Meda"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "find employees"
                Output: {{"fields": [], "all_fields_given": false, "message_to_user": "Please specify what criteria you'd like to search by (name, department, office location, etc.)"}}
                
                Input: "show me data"
                Output: {{"fields": [], "all_fields_given": false, "message_to_user": "Please specify which employees you'd like to see information for"}}
                
                Input: "I want employee info"
                Output: {{"fields": [], "all_fields_given": false, "message_to_user": "Please provide search criteria such as employee name, department, office location, or other details"}}
                
                Input: "pls show me my details"
                Output: {{"fields": [{{"field_name": "contactNo", "field_value": "[extract the number from 'Contact Number: [number]' in employee_record]"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "my info", "my profile", "show me my information", "what's my details", "my employee details"
                Output: {{"fields": [{{"field_name": "contactNo", "field_value": "[extract the number from 'Contact Number: [number]' in employee_record]"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "what is my email", "my email", "what's my email address"
                Output: {{"fields": [{{"field_name": "contactNo", "field_value": "[extract the number from 'Contact Number: [number]' in employee_record]"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "what is my role", "my role", "what's my role", "my designation"
                Output: {{"fields": [{{"field_name": "contactNo", "field_value": "[extract the number from 'Contact Number: [number]' in employee_record]"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "what is my department", "my department", "what's my department"
                Output: {{"fields": [{{"field_name": "contactNo", "field_value": "[extract the number from 'Contact Number: [number]' in employee_record]"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "what is my company", "my company", "what's my company"
                Output: {{"fields": [{{"field_name": "contactNo", "field_value": "[extract the number from 'Contact Number: [number]' in employee_record]"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "what is my manager", "my manager", "who is my manager", "my reporting manager"
                Output: {{"fields": [{{"field_name": "contactNo", "field_value": "[extract the number from 'Contact Number: [number]' in employee_record]"}}], "all_fields_given": true, "message_to_user": ""}}
                
                Input: "pls give me all employees reporting to me", "show me my team", "who reports to me", "my direct reports"
                Output: {{"fields": [{{"field_name": "reporting_manager_name", "field_value": "{employee_record.name}"}}], "all_fields_given": true, "message_to_user": ""}}
                
                FIELD MAPPING GUIDE:
                - Name variations: "Ahmad Meda", "John Smith" → "name"
                - Department: "Engineering", "HR", "Sales" → "department_name"  
                - Office/Location: "Dubai", "New York office" → "office_location_name"
                - Company: "TechCorp", "Google" → "company_name"
                - Job title: "CEO", "Manager", "Developer" → "designation"
                - Manager: "reports to John" → "reporting_manager_name"
                - Email: "john@company.com" → "emailId"
                - Gender: "male", "female" → "gender"
                - Contact: phone numbers → "contactNo"
                - Role: "Admin", "User" → "role_name"
                - Group: team/group names → "group_name"
                - Work policy: "Remote", "Hybrid" → "work_policy_name"
                - Dates: birth/joining dates → "dateOfBirth"/"dateOfJoining"
                - Check-in status: → "checked_in"/"checked_out"
                
                EDGE CASES:
                - If no search criteria found, return empty fields list and set all_fields_given to false
                - Provide helpful message_to_user when information is missing
                - Handle multiple search criteria in single query
                - IMPORTANT: Any valid field-value pair is sufficient for search - set all_fields_given to true
                - Only set all_fields_given to false for completely vague requests like "find employees" or "show data"
                - Use null for missing/unknown information
                - Extract partial information when available
                - When user says "my details", "my profile", "show me my details", etc., use the contact_number parameter provided above as the field_value for contactNo field.
                """
            )
        }
    ] + messages

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=get_employee_values
    )

    return completion.choices[0].message.parsed

def get_employee_chat(messages: list, error_dict: dict, employee_details: str):

    system_message = [
        {
            "role": "system",
            "content": (
                f"""
                The employee has asked for a READ operation on the employee details. You are an agent who will display the fetched details to the user as given based on his query: {employee_details} as a fiendly, no emoji, professional message that is being displayed in whatsapp.

                Here is the users query: {messages}
                These are the fetched details which need to be displayed along with the fields with no value: {employee_details}
                These are the error details, sometimes there is an error which needs to be informed to the user: {error_dict}

                If the employes fetched number more than 10 then tell the user to access the full list at huse.app/employees in whatsapp format.

                IMPORTANT: The system uses fuzzy matching to find results, so if the user typed something with typos or slight variations (like "software enginner" instead of "Software Engineer"), the search will still find matching employees. If employee details are provided, it means the search was SUCCESSFUL regardless of minor spelling differences.

                Now please display whatever he needed and inform him the employees details queried from his query. inform the user the users of the error if there are errors present, don't say, no errors were found if there are no errors. If employee details are present, always treat it as a successful search. This is in whatsapp chat so give no hint of you being an agent.
                Making changes to the given employee data is NOT allowed."""

            )
        }
    ]     

    completion = client.beta.chat.completions.parse(
        model=model, 
        messages=system_message,
        response_format=get_employee_chat_message
    )

    return completion.choices[0].message.parsed

def update_employee_end_response(messages: list):
    
    system_message = [
        {
            "role": "system",
            "content": (
                f"""
                The user is process of updating an employee information, if the user explicitly says he wants to leave the update employee only then change the Boolean to True.
                If the boolean is True, generate a message to the user on farewell. You are only allowed to make the boolean true only if the user says he wants to exit the update employee.
                """
            )
        }
    ] + messages

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=UpdateEmployeeEndResponse
    )

    return completion.choices[0].message.parsed

def ask_user_what_else_to_update(extracted_fields_and_values: list, result: dict, list_of_fields_with_no_value: list, fields_not_confirmed: dict):
    
    system_message = [
        {
            "role": "system",
            "content": (
                f""" You are tasked to generate a very short easy to read reply to the user who is trying to update an employee as human like HR Assistant.
                
                1- fields and field values the user wants to update: {extracted_fields_and_values}
                2- fields the wants to update but has not provided the value: {list_of_fields_with_no_value}
                3- These fields havent been updated in the database yet and are awaiting confirmation.Ask the user confirmation for these fields and their values if he is sure.: {fields_not_confirmed}
                4- result of the update of step 1: {result}


                to update an employee, you need the field and its new value. Based on the information given, ask the user if any field value of a field is not given. If the user has given fields anf their 
                new values then look at the result and inform the user if the update was successful or if if any error was present. Generate a short, no emoji, whatsapp cheerful message to the user based on all the provided details. 

                """
            )
        }
    ] 

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=AskUserWhatElseToUpdate
    )

    return completion.choices[0].message.parsed

# extra = (
#     """ Your job is to display the employee details in a friendly, casual way in whatsapp chat.

#         Using supporting knowledge, create a friendly, casual WhatsApp message to the user.

#         If Employee details are present, always treat it as a successful search.
        
#         If the user has provided any errors, inform them about the errors in a friendly way. This applies only if there are errors present.
        
#         If you have the information, do not say "I don't have that information" or "I cannot answer that at the moment."

#         Make sure to format the message in a way that is easy to read on WhatsApp, using line breaks and bullet points if necessary."""
# )


def update_employee_fields_only(messages: list):
    
    system_message = [
        {
            "role": "system",
            "content": (
                f"""
                You are a data extraction assistant used to identify which fields the user explicitly said he wants to update.Do not capture the fields that the user has provided to identify the employee. Do not capture fields that user doesnt intend to update. Change the fields that the user want to update to true.
                """
            )
        }
    ] + messages

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=EmployeeUpdateFields
    )

    return completion.choices[0].message.parsed

def ask_user_for_confirmation(messages: list):
    
    system_message = [
        {
            "role": "system",
            "content": (
                f""" The user has been asked for confirmation to delete an employee, if the user wants to delete the employee, change the Boolean to True. If he doesnt then change the boolean to False and generate a message to the user on farewell.
                """
            )
        }
    ] + messages

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=AskUserForConfirmation
    )

    return completion.choices[0].message.parsed

def ask_user_for_confirmation_to_add_employee(messages: list):
    
    system_message = [
        {
            "role": "system",
            "content": (
                f""" The user has been asked for confirmation to add an employee, if the user wants to add the employee, change the Boolean to True. If he doesnt then change the boolean to False and generate a message to the user on farewell.
                IMPORTANT:when the user wants to edit the employee, the boolean does_user_want_to_add_the_employee cannot be true as something needs to be fixed.
                """
            )
        }
    ] + messages

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=AskUserForConfirmationToAddEmployee
    )

    return completion.choices[0].message.parsed

def ask_user_for_confirmation_to_update_employee(messages: list):
    
    system_message = [
        {
            "role": "system",
            "content": (
                f"""The user has been asked for confirmation the changes he wants to make to the employee, if the user wants to update the employee with the asked changes or agrees to atleast one of the changes, change the boolean to True.
                If the user says that the employee he is trying to update is wrong, change the boolean is_the_employee_to_update_wrong to true else keep it None.

                """
            )
        }
    ] + messages

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=AskUserForConfirmationToUpdateEmployee
    )

    return completion.choices[0].message.parsed

def ask_user_for_confirmation_to_clear_employee_draft(messages: list):
    
    system_message = [
        {
            "role": "system",
            "content": (
                f""" The user has been asked that a draft is already present and if he wants to continue filling that draft or wants to add a new employee by clearing the previous draft. if the user says yes, please change the boolean to true.
                """
            )
        }
    ] + messages

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=AskUserForConfirmationToClearEmployeeDraft
    )

    return completion.choices[0].message.parsed

def does_user_want_to_exit_add_employee(messages: list):
    
    system_message = [
        {
            "role": "system",
            "content": (
                f"""Change the boolean to true only when the user explicitly says he wants to exit the add employee flow. Only if the yser explicilty says he wants to leave or exit then the boolean is true.
                 Example: "Ill add it later" Boolean will be true.
                 """
            )
        }
    ] + messages

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=IntentToExitEmployee
    )

    return completion.choices[0].message.parsed