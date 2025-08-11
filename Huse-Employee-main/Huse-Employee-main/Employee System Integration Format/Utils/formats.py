from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal

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
    office_location_name: Optional[str] = None
    company_name: Optional[str] = None
    role: Optional[str] = None
    reporting_manager_name: Optional[str] = None
    department_name: Optional[str] = None

class SoftDeleteExtraction(BaseModel):
    employee_name: Optional[str] = None
    contact_number: Optional[str] = None

class SoftDeleteEmployeeResponse(BaseModel):
    message_to_user: str = ""

class UpdateEmployeeResponse(BaseModel):
    message_to_user: str = ""

class UpdateEmployeeExtraction(BaseModel):
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
    office_location_name: Optional[str] = None
    company_name: Optional[str] = None
    role: Optional[str] = None
    reporting_manager_name: Optional[str] = None
    department_name: Optional[str] = None

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
    first_name: Optional[bool] = False
    last_name: Optional[bool] = False
    middle_name: Optional[bool] = False
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