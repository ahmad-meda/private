from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from Utils.choices import EmployeeChoices

class EmployeeAgent(BaseModel):
    """Response model for agent messages to user"""
    message_to_user: str = ""

class EmployeeData(BaseModel):
    full_name: Optional[str] = None
    contact_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    emailId: Optional[str] = None
    designation: Optional[str] = None
    dateOfJoining: Optional[str] = None
    dateOfBirth: Optional[str] = None
    gender: Optional[str] = None
    work_policy_name: Optional[str] = None
    home_latitude: Optional[float] = None
    home_longitude: Optional[float] = None
    office_location_name: Optional[str] = Field(description="The user can either provide the name of office location or provide the home coordinates(if they choose this then extract the office location as 'home_coordinates') or may refuse to give the office location (this is a privilege only for managers), so if they choose the manager-skip extract the office location as 'manager_skip'")
    company_name: Optional[str] = None
    role: Optional[str] = None
    reporting_manager_name: Optional[str] = None
    department_name: Optional[str] = None
    restrict_to_allowed_locations: Optional[bool] = Field(description="This is True if the user wants multiple office locations for the employee.")
    allow_site_checkin: Optional[bool] = Field(description="This is True if the employee is allowed to check-in from any location otherwise False.")
    reminders: Optional[bool] = Field(description="This is True if the employee wants reminders for check-in and check-out.")
    is_hr: Optional[bool] = Field(description="This is True if the employee being added is an HR.")
    hr_scope: Optional[str] = Field(description="This is the scope of the HR. It can be 'company' or 'group'.")
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
    full_name: Optional[str] = None
    contact_number: Optional[str] = None
    first_name: Optional[str] = Field(description="only extract this if the  user only mentions the first name of the employee to update.")
    last_name: Optional[str] = Field(description="only extract this if the  user only mentions the last name of the employee to update.")
    middle_name: Optional[str] = Field(description="only extract this if the  user only mentions the middle name of the employee to update.")
    emailId: Optional[str] = None
    designation: Optional[str] = None
    dateOfJoining: Optional[str] = None
    dateOfBirth: Optional[str] = None
    gender: Optional[str] = None
    work_policy_name: Optional[str] = None
    home_latitude: Optional[float] = None
    home_longitude: Optional[float] = None
    office_location_name: Optional[str] = None
    company_name: Optional[str] = None
    role: Optional[str] = Field(None, options=EmployeeChoices.get_role_choices())
    reporting_manager_name: Optional[str] = None
    department_name: Optional[str] = None
    restrict_to_allowed_locations: Optional[bool] = Field(description="This is True if the user wants multiple office locations for the employee.")
    allow_site_checkin: Optional[bool] = Field(description="This is True if the employee is allowed to check-in from any location otherwise False.")
    reminders: Optional[bool] = Field(description="This is True if the employee wants reminders for check-in and check-out.")
    is_hr: Optional[bool] = Field(description="This is True if the employee being added is an HR.")
    hr_scope: Optional[str] = Field(description="This is the scope of the HR. It can be 'company' or 'group'.")

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
    full_name: Optional[bool] = False
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
    does_user_want_to_add_the_employee: bool
    farewell_message_to_user: Optional[str] = Field(description="This is the message to the user if say anything other than yes to the confirmation.")
    did_user_mention_editing_employee_details: Optional[bool] = Field(description="This is True if the user mentions another employee to add after saying no to the confirmation.")

class AskUserForConfirmationToUpdateEmployee(BaseModel):
    does_user_want_to_update_the_employee: bool = Field(description="This is True if the user wants to update the employee with the asked changes.")
    farewell_message_to_user: Optional[str] = Field(description="This is the message to the user if say anything other than yes to the confirmation.")
    did_user_mention_editing_employee_details: Optional[bool] = Field(description="This is only True if the user mentions that he wants to update any other field after the confirmation")