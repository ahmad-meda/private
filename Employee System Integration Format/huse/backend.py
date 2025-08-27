from typing import Dict, Any
from Utils.huse_app_helpers import prepare_huse_data, get_security_question, make_huse_api_request
from huse.credentials import generate_credentials
from proxies.proxy import EmployeeProxy


def register_employee_in_huse(employee_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Register a new employee in the Huse app
    """
    base_url = "http://15.185.143.138:5001"
    token = "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjpbIlNVUEVSIiwiU3VwZXJBZG1pbiJdLCJuYW1laWQiOiIxIiwidW5pcXVlX25hbWUiOiJzdXBlciIsIm5iZiI6MTc1MDkzNDIwNCwiZXhwIjoxNzgyNDcwMjA0LCJpYXQiOjE3NTA5MzQyMDR9.K49nAhAOwSCECfq4x6E780bcDER2fIeTEBhDeUVznm-3yjwwZ8exWZv8FEl9p3FcVAKPk4LL_LIR5wbicuuaEw"
    
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
            print(EmployeeProxy.add_employee_to_huse(employee_data.get('id'), username, plain_password))    
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

