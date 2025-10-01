from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from Utils.choices import EmployeeChoices

class EmployeeAgent(BaseModel):
    """Response model for agent messages to user"""
    message_to_user: str = ""

class EmployeeData(BaseModel):
    full_name: Optional[str] = Field(description="This is the name of the employee to be added. Extract this if the user gives a first name or first and last name or first last and middle name.")
    contact_number: Optional[str] = Field(description="This is the contact number of the employee to be added. Extract this if the user gives a contact number.")
    first_name: Optional[str] = Field(description="This is the first name of the employee to be added. Extract this if the user gives a first name.")
    last_name: Optional[str] = Field(description="This is the last name of the employee to be added. Extract this if the user gives a last name.")
    middle_name: Optional[str] = Field(description="This is the middle name of the employee to be added. Extract this if the user gives a middle name.")
    emailId: Optional[str] = Field(description="This is the email of the employee to be added. Extract this if the user gives an email.")
    designation: Optional[str] = Field(description="This is the designation of the employee to be added. Extract this if the user gives a designation.")
    dateOfJoining: Optional[str] = Field(description="This is the date of joining of the employee to be added. Extract this if the user gives a date of joining.")
    dateOfBirth: Optional[str] = Field(description="This is the date of birth of the employee to be added. Extract this if the user gives a date of birth.")
    gender: Optional[str] = Field(description="This is the gender of the employee to be added. Extract this if the user gives a gender.")
    work_policy_name: Optional[str] = Field(description="This is the work policy of the employee to be added. Extract this if the user gives a work policy.")
    home_latitude: Optional[float] = Field(description="This is the home latitude of the employee to be added. Extract this if the user gives a home latitude.")
    home_longitude: Optional[float] = Field(description="This is the home longitude of the employee to be added. Extract this if the user gives a home longitude.")
    office_location_name: Optional[str] = Field(description="The user can either provide the name of office location or provide the home coordinates(if they choose this then extract the office location as 'home_coordinates') or may refuse to give the office location (this is a privilege only for managers), so if they choose the manager-skip extract the office location as 'manager_skip'")
    company_name: Optional[str] = Field(description="This is the company of the employee to be added. Extract this if the user gives a company.")
    role: Optional[str] = Field(description="This is the role of the employee to be added. Extract this if the user gives a role.")
    reporting_manager_name: Optional[str] = Field(description="This is the reporting manager of the employee to be added. Extract this if the user gives a reporting manager.")
    department_name: Optional[str] = Field(description="This is the department of the employee to be added. Extract this if the user gives a department.")
    restrict_to_allowed_locations: Optional[bool] = Field(description="This is True if the user wants multiple office locations for the employee.")
    allow_site_checkin: Optional[bool] = Field(description="This is True if the employee is allowed to check-in from any location otherwise False.")
    reminders: Optional[bool] = Field(description="This is True if the employee wants reminders for check-in and check-out. Extract this if the user gives a reminder.")
    is_hr: Optional[bool] = Field(description="This is True if the employee being added is an HR.")
    hr_scope: Optional[str] = Field(description="This is the scope of the HR. It can be 'company' or 'group'. Extract this if the user gives a scope.")
    multiple_office_locations_to_check_in: Optional[List[str]] = Field(description="This is a list of office locations to check-in from. The bot will ask the user the multiple office locations for the employee to checkin from. The user will give names of the office locations to check-in from.")

class SoftDeleteExtraction(BaseModel):
    employee_name: Optional[str] = Field(description="The name of the single employee to be deleted.")
    contact_number: Optional[str] = Field(description="The contact number of the employee to be deleted.")
    email: Optional[str] = None

class SoftDeleteEmployeeResponse(BaseModel):
    message_to_user: str = ""

class UpdateEmployeeResponse(BaseModel):
    message_to_user: str = ""

class UpdateEmployeeExtraction(BaseModel):
    full_name: Optional[str] = Field(description="This is the full name of the employee to update. Do not extract this if the user replies no to updating this field after confirmation.")
    contact_number: Optional[str] = Field(description="This is the contact number of the employee to update. Do not extract this if the user replies no to updating field after confirmation.")
    first_name: Optional[str] = Field(description="only extract this if the  user only mentions the first name of the employee to update.")
    last_name: Optional[str] = Field(description="only extract this if the  user only mentions the last name of the employee to update.")
    middle_name: Optional[str] = Field(description="only extract this if the  user only mentions the middle name of the employee to update.")
    emailId: Optional[str] = Field(description="This is the email of the employee to update. Do not extract this if the user replies no to updating this field after confirmation.")
    designation: Optional[str] = Field(description="This is the designation of the employee to update. Do not extract this if the user replies no to updating this field after confirmation.")
    dateOfJoining: Optional[str] = Field(description="This is the date of joining of the employee to update. Do not extract this if the user replies no to updating field after confirmation.")
    dateOfBirth: Optional[str] = Field(description="This is the date of birth of the employee to update. Do not extract this if the user replies no to updating this field after confirmation.")
    gender: Optional[str] = Field(description="This is the gender of the employee to update. Do not extract this if the user replies no to updating this field after confirmation.")
    work_policy_name: Optional[str] = Field(description="This is the work policy of the employee to update. Do not extract this if the user replies no to updating this field after confirmation.")
    home_latitude: Optional[float] = Field(description="This is the home latitude of the employee to update. Do not extract this if the user replies no to updating field after confirmation.")
    home_longitude: Optional[float] = Field(description="This is the home longitude of the employee to update. Do not extract this if the user replies no to updating this field after confirmation.")
    office_location_name: Optional[str] = Field(description="This is the office location of the employee to update. Do not extract this if the user replies no to updating this field after confirmation.")
    company_name: Optional[str] = Field(description="This is the company of the employee to update. Do not extract this if the user replies no to updating this field after confirmation.")
    role: Optional[str] = Field(description="This is the role of the employee to update. Do not extract this if the user replies no to updating this field after confirmation.")
    reporting_manager_name: Optional[str] = Field(description="This is the reporting manager of the employee to update. Do not extract this if the user replies no to updating this field after confirmation.")
    department_name: Optional[str] = Field(description="This is the department of the employee to update. Do not extract this if the user replies no to updating this field after confirmation.")
    restrict_to_allowed_locations: Optional[bool] = Field(description="This is True if the user wants multiple office locations for the employee. Do not extract this if the user replies no to updating this field after confirmation. This is False if the user wants to update the office location of the employee.")
    allow_site_checkin: Optional[bool] = Field(description="This is True if the employee is allowed to check-in from any location otherwise False. Do not extract this is the the user replies no to updating this field after confirmation.")
    reminders: Optional[bool] = Field(description="This is True if the employee wants reminders for check-in and check-out. Do not extract this if the user replies no to updating this field after confirmation.")
    is_hr: Optional[bool] = Field(description="This is True if the employee being added is an HR. Do not extract this if the user replies no to updating this field after confirmation.")
    hr_scope: Optional[str] = Field(description="This is the scope of the HR. It can be 'company' or 'group'. Do not extract this if the user replies no to updating this field after confirmation.")

class LocateUpdateEmployeeResponse(BaseModel):
    current_phone_number: Optional[str] = None
    current_name: Optional[str] = None
    current_email: Optional[str] = None #------------------------------ FIX THIS

class SkippedDetails(BaseModel):
    skipped_fields: Optional[List[str]] = None

class db_employee_fields(BaseModel):
    employeeId: Optional[str] = None
    name: Optional[str] = None
    emailId: Optional[str] = None
    designation: Optional[str] = None
    dateOfJoining: Optional[str] = None
    dateOfBirth: Optional[str] = None
    contactNo: Optional[str] = None
    gender: Optional[str] = None
    office_location_name: Optional[str] = None
    work_policy_name: Optional[str] = None
    home_latitude: Optional[str] = None
    home_longitude: Optional[str] = None
    company_name: Optional[str] = None      
    group_name: Optional[str] = None
    reporting_manager_name: Optional[str] = None
    role_name: Optional[str] = None
    department_name: Optional[str] = None
    checked_in: Optional[str] = None
    checked_out: Optional[str] = None

class get_employee_fields(BaseModel):
    fields: List[db_employee_fields]
    field_name:str
    field_value: str

class get_employee_values(BaseModel):
    fields: list[get_employee_fields]
    all_fields_given: bool
    message_to_user: str

class get_employee_chat_message(BaseModel):
    message_to_user: str

class UpdateEmployeeEndResponse(BaseModel):
    does_user_want_end_interaction: bool
    farwell_message_to_user: str

class AskUserWhatElseToUpdate(BaseModel):
    message_to_user: str

class EmployeeSelectionExtraction(BaseModel):
    is_user_selecting: bool
    selected_employee_database_id: Optional[int] = None
    confidence: int  # 1-100 scale

class EmployeeUpdateFields(BaseModel):
    full_name: Optional[bool] = Field(description="This is True only if the user explicitly says that users wants to update the full name of the employee.")
    contact_number: Optional[bool] = False
    first_name: Optional[bool] = Field(description="This is True if the user wants to update the first name of the employee. do not extract this if the user mentions the full name of the employee to update.")
    last_name: Optional[bool] = Field(description="This is True if the user wants to update the last name of the employee. do not extract this if the user mentions the full name of the employee to update.")
    middle_name: Optional[bool] = Field(description="This is True if the user wants to update the middle name of the employee. do not extract this if the user mentions the full name of the employee to update.")
    emailId: Optional[bool] = False
    designation: Optional[bool] = False
    dateOfJoining: Optional[bool] = False
    dateOfBirth: Optional[bool] = False
    gender: Optional[bool] = False
    work_policy_name: Optional[bool] = False
    home_latitude: Optional[bool] = False
    home_longitude: Optional[bool] = False
    office_location_name: Optional[bool] = False
    company_name: Optional[bool] = False
    role: Optional[bool] = False
    reporting_manager_name: Optional[bool] = False
    department_name: Optional[bool] = False
    restrict_to_allowed_locations: Optional[bool] = Field(description="This is True if the user wants multiple office locations for the employee.")
    allow_site_checkin: Optional[bool] = Field(description="This is True if the employee is allowed to check-in from any location otherwise False.")
    reminders: Optional[bool] = Field(description="This is True if the employee wants reminders for check-in and check-out.")
    is_hr: Optional[bool] = Field(description="This is True if the employee being added is an HR.")
    hr_scope: Optional[str] = Field(description="This is the scope of the HR. It can be 'company' or 'group'.")
    

class AskUserForConfirmation(BaseModel):
    does_user_want_to_delete: bool
    farewell_message_to_user: Optional[str] = Field(description="This is the message to the user if say anything other than yes to the confirmation.")
    did_user_mention_another_employee: Optional[bool] = Field(description="This is True if the user mentions another employee to delete after saying no to the confirmation.")


class AskUserForConfirmationToAddEmployee(BaseModel):
    does_user_want_to_add_the_employee: bool = Field(description="This is True if the user wants to add the employee and doesnt mention any changes tot he displayed employee data.")
    farewell_message_to_user: Optional[str] = Field(description="This is the message to the user if say anything other than yes to the confirmation.")
    did_user_mention_editing_employee_details: Optional[bool] = Field(description="This is True if the user mentions another employee to add after saying no to the confirmation.")

class AskUserForConfirmationToUpdateEmployee(BaseModel):
    does_user_want_to_update_the_employee: bool = Field(description="This is True if the user wants to update the employee with the asked changes. This is true if the employee agress to one change when asked for many , if for example, asked for email and contact, but only said yes to contact, so this is boolean will be true.")
    farewell_message_to_user: Optional[str] = Field(description="This is the message to the user if say anything other than yes to the confirmation.")
    did_user_mention_editing_employee_details: Optional[bool] = Field(description="This is only True if the user mentions that he wants to update any other field after the confirmation. This also true if the user wishes to correct the field value asking for confirmation.")

class AskUserForConfirmationToClearEmployeeDraft(BaseModel):
    does_user_want_to_clear_the_draft: bool = Field(description="This is True if the user wants to clear the draft. if the user wamts to continue with the previous draft then its False")
    is_user_intent_clear: bool = Field(description="If the users reply doesnt convey their intent if they want to clear the draft or not, then this is True")
    message_when_intent_not_clear: Optional[str] = Field(description="This is the message to the user if the boolean is_user_intent_clear is True. Asking them if they want to clear the draft or not.")