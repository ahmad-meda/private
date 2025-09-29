import requests
from typing import Dict, Any, Optional
from huse.credentials import generate_security_answer
from dotenv import load_dotenv
import os

load_dotenv()


def prepare_huse_data(employee_data: Dict[str, Any], security_question: str, username: str, plain_password: str) -> Dict[str, Any]:
    """
    Prepare employee data for the Huse API format
    
    Args:
        employee_data: Employee data from the database
        security_question: Security question from API
        username: Generated username
        plain_password: Generated password
        
    Returns:
        Formatted data for Huse API
    """
    # Get full name directly from the name column
    full_name = employee_data.get('name')
    
    # Extract email
    email = employee_data.get('emailId')
    
    # Generate contact number
    contact = employee_data.get('contactNo')
    
    # Map gender (API expects capitalized values: Male, Female, Other)
    gender = employee_data.get('gender')
    
    # Generate unique security answer based on employee name and ID
    employee_id = employee_data.get('employeeId')  # Use the employee's public ID
    security_answer = generate_security_answer(full_name, employee_id)
    
    # Prepare the data according to Huse API requirements
    huse_data = {
        "name": full_name,
        "email": email,
        "username": username,
        "contact": contact,
        "gender": gender,
        "terms": "accepted",  # Default value
        "password": plain_password,  # Use generated password
        "securityQuestion": security_question,
        "securityAnswer": security_answer  # Generated unique answer
    }
    
    # Validate that all required fields are present and not empty
    required_fields = ["name", "email", "username", "contact", "gender", "terms", "password", "securityQuestion", "securityAnswer"]
    missing_fields = []
    
    for field in required_fields:
        if not huse_data.get(field):
            missing_fields.append(field)
    
    if missing_fields:
        raise ValueError(f"Missing required fields for Huse API: {', '.join(missing_fields)}")
    
    return huse_data


def get_security_question(base_url: str, headers: Dict[str, str], cached_question: Optional[str] = None) -> str:
    """
    Fetch security question from the Huse API
    
    Args:
        base_url: Base URL for the API
        headers: Request headers
        cached_question: Previously cached question
        
    Returns:
        Security question string
    """
    if cached_question:
        return cached_question
        
    try:
        url = f"{base_url}/api/Questions"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            questions = response.json()
            if questions and len(questions) > 0:
                # Get the first question's statement
                security_question = questions[0].get('statement')
                if security_question:
                    print(f"Fetched security question from API: {security_question}")
                    return security_question
                else:
                    print("No statement found in the first question")
                    raise Exception("No statement found in API response")
            else:
                print("No questions found in API response")
                raise Exception("No questions found in API response")
        else:
            print(f"Failed to fetch security question. Status: {response.status_code}")
            raise Exception(f"API request failed with status: {response.status_code}")
            
    except Exception as e:
        print(f"Error fetching security question: {str(e)}")
        raise Exception(f"Failed to get security question from API: {str(e)}")


def make_huse_api_request(url: str, data: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Make API request to Huse app
    
    Args:
        url: API endpoint URL
        data: Request data
        headers: Request headers
        
    Returns:
        Dictionary containing the API response
    """
    try:
        print(f"Huse API URL: {url}")
        print(f"Huse API Data: {data}")
        print(f"Huse API Headers: {headers}")
        
        response = requests.post(url, data=data, headers=headers)
        print(f"Huse API Response Status: {response.status_code}")
        print(f"Huse API Response: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json() if response.text else {}
            return {
                "success": True,
                "message": "Employee successfully registered in Huse",
                "data": response_data,
                "credentials": {
                    "username": data.get("username"),
                    "password": data.get("password")
                }
            }
        else:
            return {
                "success": False,
                "message": f"Failed to register employee in Huse. Status: {response.status_code}",
                "error": response.text
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error registering employee in Huse: {str(e)}",
            "error": str(e)
        }
