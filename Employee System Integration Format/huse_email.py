from proxies.proxy import EmployeeProxy
from huse.backend import register_employee_in_huse
from huse.email import send_huse_credentials_email
from huse.backend import huse_update_employee_status

def send_employee_credentials_email(id):
    # Basic input validation
    if not id or not isinstance(id, int) or id <= 0:
        print("Error: Invalid employee ID")
        return

    # Get employee record
    try:
        employee_obj = EmployeeProxy.get_employee_record_by_id(id)
    except Exception as e:
        print(f"Error: Failed to retrieve employee record - {str(e)}")
        return

    if not employee_obj:
        print(f"Error: Employee with ID {id} not found in database")
        return

    # Check essential fields
    if not employee_obj.name or not employee_obj.emailId:
        print("Error: Employee missing essential data (name or email)")
        return

    print(employee_obj)

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
    try:
        result = register_employee_in_huse(employee_data)
    except Exception as e:
        print(f"Error: Failed to register employee in HUSE - {str(e)}")
        return

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
        
        try:
            response = send_huse_credentials_email(
                employee=employee_data.get('name'),
                employee_emails=[employee_data.get('emailId')],
                username=credentials.get('username'),
                password=credentials.get('password'),
                security_question=huse_data.get('securityQuestion'),
                security_answer=result.get('security_answer')  # Use locally generated security answer
            )
            
            # Check if email sending was successful
            if response and response.get('success'):
                print("SUCCESS: Credentials email sent successfully!")
            else:
                print(f"Error: Email sending failed - {response.get('message', 'Unknown error') if response else 'No response from email service'}")
                return
                
        except Exception as e:
            print(f"Error: Failed to send credentials email - {str(e)}")
            return
        
        # Change the status of the account created for the employee to active - "3" is the status for active accounts.
        huse_user_id = result.get('data', {}).get('id')
        status_updated = False
        status_message = ""
        
        if huse_user_id:
            try:
                status_result = huse_update_employee_status(user_id=huse_user_id, status=3)
                print(f"Status update result: {status_result}")
                if status_result and status_result.get('success'):
                    status_updated = True
                    status_message = "Account activated successfully"
                else:
                    status_message = f"Status update failed: {status_result.get('message', 'Unknown error') if status_result else 'No response'}"
            except Exception as e:
                status_message = f"Status update error: {str(e)}"
        
        # Return success with all details (sensitive data masked)
        return {
            "success": True,
            "message": "Employee successfully registered, credentials emailed, and account activated",
            "details": {
                "employee_name": employee_data.get('name'),
                "email_address": employee_data.get('emailId'),
                "username": credentials.get('username'),
                "password": "[REDACTED]",
                "security_question": huse_data.get('securityQuestion'),
                "security_answer": "[REDACTED]",
                "employee_id": employee_data.get('id'),
                "huse_user_id": huse_user_id,
                "email_sent": True,
                "status_updated": status_updated,
                "status_message": status_message
            }
        }
    else:
        print(f"Error: HUSE registration failed - {result.get('message', 'Unknown error') if result else 'No response from HUSE'}")
        return {
            "success": False,
            "message": f"HUSE registration failed: {result.get('message', 'Unknown error') if result else 'No response from HUSE'}",
            "error": "HUSE_REGISTRATION_FAILED"
        }