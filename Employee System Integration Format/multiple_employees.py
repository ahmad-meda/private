from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from openai import OpenAI   
import os   
from Utils.ai_client import client

model = "gpt-4o-mini"

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

class MultipleEmployeeData(BaseModel):
    employees: List[EmployeeData]

def extract_data(messages):
        extraction_messages = [
            {
                "role": "system",
                "content": (

                    """You are a data extraction assistant being used to extract data given by the user about an employee. The user may give one or multiple employee data to add.if the user says i want to create 2 employees ahmed and mohammed u make 2 EmployeeAata objects.
                    
                    Only extract data that was explicitly provided by the user in the conversation. DO NOT invent, assume, or hallucinate any data that was not mentioned by the user. If a field was not provided by the user, leave it as null/None.
                    
                    From this conversation, extract ONLY the employee info that was actually given by the user as structured data.
                    date as postgres format (YYYY-MM-DD)
                    name saved in professional format(upper and lower case)
                    """
                )
            }
        ] + messages
        
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=extraction_messages,
            response_format=MultipleEmployeeData,
        )
        return completion.choices[0].message.parsed.employees



test_messages = [
    {
        "role": "user",
        "content": """I want to add three new employees to our system"""
        },
        {
            "role": "assistant", 
            "content": "I'll help you add these three employees to the system. whats their info"
        }
    ]

result = extract_data(test_messages)
print(len(result))
print(result)
