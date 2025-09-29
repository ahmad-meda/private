from typing import Dict, Any
from Utils.huse_app_helpers import prepare_huse_data, get_security_question, make_huse_api_request
from huse.credentials import generate_credentials
from proxies.proxy import EmployeeProxy
import requests
from dotenv import load_dotenv
import os

load_dotenv()



def register_employee_in_huse(employee_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Register a new employee in the Huse app
    """
    base_url = os.environ.get('API_BASE_URL')
    token = os.environ.get('API_AUTH_TOKEN')
    
    headers = {"Authorization": token, "Content-Type": "application/json"}
    form_headers = {"Authorization": token}
    
    try:
        # Get full name from employee data
        full_name = employee_data.get('name')
        
        # Generate credentials
        username, plain_password, _ = generate_credentials(full_name)
        
        # Get security question from API
        security_question = get_security_question(base_url, headers)
        
        # Prepare data for Huse API
        huse_data = prepare_huse_data(employee_data, security_question, username, plain_password)
        
        # Store the security answer for later use in email
        security_answer = huse_data.get('securityAnswer')
        print(f"DEBUG - Security answer stored: '{security_answer}'")
        
        # Make API request
        url = f"{base_url}/api/Users/register"
        response = make_huse_api_request(url, huse_data, form_headers)
        print(response)
        if response.get('success') is True:
            huse_app_id = response.get('data', {}).get('id')
            print(EmployeeProxy.add_employee_to_huse(employee_data.get('id'), huse_app_id, username, plain_password))    
            # Add the locally generated security answer to the response
            response['security_answer'] = security_answer
            return response
        else:
            return response 
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error registering employee in Huse: {str(e)}",
            "error": str(e)
        }

def huse_update_employee_status(user_id: int, status: int, remarks: str = None) -> Dict[str, Any]:
    """
    Update employee status in the Huse app
    
    Args:
        user_id: The user ID to update
        status: The new account status (integer)
        remarks: Optional remarks for the status change
        
    Returns:
        Dictionary containing the API response
    """
    base_url = os.environ.get('API_BASE_URL')
    token = os.environ.get('API_AUTH_TOKEN')
    
    headers = {"Authorization": token}
    
    try:
        # Prepare form data for the API request
        form_data = {
            "UserId": str(user_id),
            "AccountStatus": str(status)
        }
        
        # Add remarks if provided
        if remarks:
            form_data["Remarks"] = remarks
        
        # Make PUT request to update status endpoint
        url = f"{base_url}/api/Users/update_status"
        
        print(f"Updating user status - URL: {url}")
        print(f"Form data: {form_data}")
        
        response = requests.put(url, data=form_data, headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json() if response.text else {}
            return {
                "success": True,
                "message": "Employee status successfully updated in Huse",
                "data": response_data
            }
        else:
            return {
                "success": False,
                "message": f"Failed to update employee status in Huse. Status: {response.status_code}",
                "error": response.text
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error updating employee status in Huse: {str(e)}",
            "error": str(e)
        }