import os
import pandas as pd
import requests
import random
from datetime import datetime
from dotenv import load_dotenv
from Files.SQLAlchemyModels import Employee, SessionLocal
from huse.backend import register_employee_in_huse, huse_update_employee_status
from huse.email import send_huse_credentials_email
from Utils.huse_app_helpers import get_security_question
from Utils.password_helpers import generate_username, split_name

from proxies.proxy import EmployeeProxy

load_dotenv()

def get_huse_users():
    """Get users from Huse API with validation"""
    try:
        # Validate environment variables
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        if not base_url or not token:
            print("Error: API_BASE_URL and API_AUTH_TOKEN must be set")
            return None
        
        # Validate URL format
        if not base_url.startswith(('http://', 'https://')):
            print("Error: API_BASE_URL must start with http:// or https://")
            return None
        
        headers = {"Authorization": token}
        url = f"{base_url}/api/Users"
        
        # Add parameters like in your curl command
        params = {
            'PageSize': 1000
        }
        
        # Make request with timeout
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            try:
                users = response.json()
                
                # Validate response format
                if not isinstance(users, list):
                    print("Error: API response is not a list")
                    return None
                
                # Extract usernames with validation
                usernames = []
                for i, user in enumerate(users):
                    if not isinstance(user, dict):
                        print(f"Warning: User at index {i} is not a dictionary, skipping")
                        continue
                    
                    if 'username' not in user:
                        print(f"Warning: User at index {i} missing 'username' field, skipping")
                        continue
                    
                    username = user['username']
                    if username and isinstance(username, str) and username.strip():
                        usernames.append(username.strip())
                    else:
                        print(f"Warning: Invalid username at index {i}: '{username}', skipping")
                
                print(f"Successfully retrieved {len(usernames)} valid usernames from Huse")
                return usernames
                
            except ValueError as e:
                print(f"Error: Invalid JSON response from API - {e}")
                return None
                
        else:
            print(f"API Error: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Error details: {error_detail}")
            except:
                print(f"Error response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("Error: API request timed out after 30 seconds")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed - {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in get_huse_users: {e}")
        return None

def check_username_in_huse(username):
    """Check if username already exists in Huse"""
    try:
        huse_usernames = get_huse_users()
        print("huse_usernames", huse_usernames)
        if huse_usernames:
            return username in huse_usernames
        return False
    except Exception as e:
        print(f"Error checking username in Huse: {e}")
        return False
    
def get_huse_users_details():
    """Get all users from Huse API"""
    try:
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        headers = {"Authorization": token}
        url = f"{base_url}/api/Users"
        params = {'PageSize': 1000}
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            users = response.json()
            print(f"Found {len(users)} users in Huse")
            return users
        else:
            print(f"API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def find_user_id_by_mobile(mobile):
    """Find user ID matching mobile number"""
    users = get_huse_users_details()
    if not users:
        return None
    
    mobile = mobile.lower().strip()
    
    for user in users:
        if not isinstance(user, dict):
            continue
        
        user_id = user.get('id')
        user_mobile = user.get('contact', user.get('phone', '')).lower().strip()
        
        # Check if mobile matches
        if mobile in user_mobile:
            return user_id
    
    return None

def find_user_id_by_email(email):
    """Find user ID matching email"""
    users = get_huse_users_details()
    if not users:
        return None
    
    email = email.lower().strip()
    
    for user in users:
        if not isinstance(user, dict):
            continue
        
        user_id = user.get('id')
        user_email = user.get('email', '').lower().strip()
        
        # Check if email matches
        if email in user_email:
            return user_id
    
    return None

def delete_user_by_id(user_id):
    """Delete a user from Huse using their ID"""
    try:
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        headers = {
            "accept": "application/json",
            "Authorization": token
        }
        
        url = f"{base_url}/api/Users/permanent/{user_id}"
        
        response = requests.delete(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ User ID {user_id} deleted successfully!")
            return True
        else:
            print(f"❌ Failed to delete user ID {user_id}: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Error details: {error_detail}")
            except:
                print(f"Error response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ Timeout deleting user ID {user_id}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error deleting user ID {user_id}: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error deleting user ID {user_id}: {e}")
        return False

def process_employees():
    """
    Process all employees:
    1. Get employees from database
    2. Save to Excel
    3. Create Huse credentials
    4. Send email with credentials  
    5. Update database with credentials
    """
    # Initialize skipped_no_email outside try block to avoid UnboundLocalError
    skipped_no_email = []
    
    try:
        # Get all employees from database
        print("Getting employees from database...")
        employees = EmployeeProxy.get_all_employees_by_company(6)
        # # employees = EmployeeProxy.get_all_employees_by_group(1)
        # # employees = EmployeeProxy.get_all_employees_by_company_list([1,2,3])
        # employees = EmployeeProxy.get_all_active_employees()

        print(f"Found {len(employees)} employees")
        
        if not employees:
            print("No employees found")
            return
        
        # Save to Excel with all details
        print("Saving employees to Excel...")
        employee_list = []
        for emp in employees:
            # Check if employee is already registered (has both username and password)
            is_registered = bool(emp.username and emp.password)
            
            employee_list.append({
                'ID': emp.id,
                'Employee ID': emp.employeeId,
                'Name': emp.name,
                'First Name': emp.first_name,
                'Middle Name': emp.middle_name,
                'Last Name': emp.last_name,
                'Email': emp.emailId,
                'Phone': emp.contactNo,
                'Designation': emp.designation,
                'Date of Joining': emp.dateOfJoining,
                'Date of Birth': emp.dateOfBirth,
                'Gender': emp.gender,
                'Company ID': emp.company_id,
                'Department ID': emp.department_id,
                'Role ID': emp.role_id,
                'Group ID': emp.group_id,
                'Office Location ID': emp.office_location_id,
                'Work Policy ID': emp.work_policy_id,
                'Home Latitude': emp.home_latitude,
                'Home Longitude': emp.home_longitude,
                'Reporting Manager ID': emp.reporting_manager_id,
                'Is HR': emp.is_hr,
                'HR Scope': emp.hr_scope,
                'Allow Site Check-in': emp.allow_site_checkin,
                'Restrict to Allowed Locations': emp.restrict_to_allowed_locations,
                'Reminders': emp.reminders,
                'Allowed Company IDs': emp.allowed_company_ids,
                'Created By': emp.created_by,
                'Is Deleted': emp.is_deleted,
                'Deleted At': emp.deleted_at,
                'App Username': emp.username,
                'App Password': emp.password,
                'Registered': str(is_registered)
            })
        
        df = pd.DataFrame(employee_list)
        excel_filename = f"employees.xlsx"
        df.to_excel(excel_filename, index=False)
        print(f"Saved to {excel_filename}")
        
        # Get API credentials
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        headers = {"Authorization": token, "Content-Type": "application/json"}
        
        # Get security question
        try:
            security_question = get_security_question(base_url, headers)
        except Exception as e:
            print(f"Failed to get security question: {e}")
            security_question = "What is your favorite color?"
        
        # Process each employee
        print("Processing employees...")
        for i, emp in enumerate(employees):
            # Skip if no email address
            if not emp.emailId or emp.emailId.strip() == '':
                print(f"Skipping {emp.name} - no email address")
                skipped_no_email.append({
                    'ID': emp.id,
                    'Name': emp.name,
                    'Employee ID': emp.employeeId,
                    'Reason': 'No email address'
                })
                continue
            
            # Skip if no contact number
            if not emp.contactNo or emp.contactNo.strip() == '':
                print(f"Skipping {emp.name} - no contact number")
                skipped_no_email.append({
                    'ID': emp.id,
                    'Name': emp.name,
                    'Employee ID': emp.employeeId,
                    'Reason': 'No contact number'
                })
                continue
            
            # Check if employee already has credentials in database
            if emp.username and emp.password:
                # Check if the existing username exists in Huse
                if check_username_in_huse(emp.username):
                    print(f"Username {emp.username} exists in Huse for {emp.name}")
                    # Get user details and check/update status to 3
                    users = get_huse_users()
                    if users:
                        for user in users:
                            if isinstance(user, dict) and user.get('username') == emp.username:
                                user_id = user.get('id')
                                current_status = user.get('status')
                                if user_id:
                                    if current_status != 3:
                                        status_result = huse_update_employee_status(user_id=user_id, status=3)
                                        if status_result.get('success'):
                                            print(f"✅ Updated status from {current_status} to 3 for {emp.name} (ID: {user_id})")
                                        else:
                                            print(f"❌ Failed to update status for {emp.name}: {status_result.get('message')}")
                                    else:
                                        print(f"✅ Status is already 3 for {emp.name} - no update needed")
                                break
                    print(f"Skipping {emp.name} - already registered and exists in Huse")
                    continue
                else:
                    print(f"Employee {emp.name} has credentials in DB but not in Huse. Generating new credentials...")
                    
                    # Check if email or contact already exists in Huse and delete if found
                    print(f"Checking for existing users with email '{emp.emailId}' or contact '{emp.contactNo}'...")

                    # Find existing user by contact
                    existing_contact_id = find_user_id_by_mobile("+" + emp.contactNo)
                    if existing_contact_id:
                        print(f"Found existing user with contact '{emp.contactNo}' (ID: {existing_contact_id}). Deleting...")
                        if delete_user_by_id(existing_contact_id):
                            print(f"✅ Deleted existing user with contact '{emp.contactNo}'")
                        else:
                            print(f"❌ Failed to delete existing user with contact '{emp.contactNo}'")
                    
                    # Find existing user by email
                    existing_email_id = find_user_id_by_email(emp.emailId)
                    if existing_email_id:
                        print(f"Found existing user with email '{emp.emailId}' (ID: {existing_email_id}). Deleting...")
                        if delete_user_by_id(existing_email_id):
                            print(f"✅ Deleted existing user with email '{emp.emailId}'")
                        else:
                            print(f"❌ Failed to delete existing user with email '{emp.emailId}'")
                    
                    
                    # If no existing users found
                    if not existing_email_id and not existing_contact_id:
                        print(f"No existing users found with email '{emp.emailId}' or contact '{emp.contactNo}'")
                    
                    # Generate new credentials and register in Huse
                    first_name, last_name = split_name(emp.name)
                    new_username = generate_username(first_name, last_name)
                    
                    # Check if the new username already exists in Huse
                    if check_username_in_huse(new_username):
                        print(f"Generated username '{new_username}' already exists in Huse for {emp.name}")
                        new_username = f"{new_username}{random.randint(1, 9999)}"  # Add random number and continue
                        print(f"Updated username to '{new_username}' for {emp.name}")
                        
                        # Check if the newly generated username also exists in Huse
                        while check_username_in_huse(new_username):
                            new_username = f"{new_username}{random.randint(1, 9999)}"
                            print(f"Username still exists, trying '{new_username}'")
                    
                    # Prepare employee data for new registration
                    contact_no = emp.contactNo or ''
                    if contact_no and not str(contact_no).startswith('+'):
                        contact_no = "+" + str(contact_no)
                    
                    # Format gender - capitalize first letter, default to "Other" if null
                    gender = emp.gender or 'Other'
                    if gender and gender.strip():
                        gender = gender.strip().capitalize()
                    else:
                        gender = 'Other'
                    
                    employee_data = {
                        'id': emp.id,
                        'name': emp.name,
                        'emailId': emp.emailId,
                        'contactNo': contact_no,
                        'gender': gender,
                        'employeeId': emp.employeeId
                    }
                    
                    # Create Huse credentials with new username
                    result = register_employee_in_huse(employee_data)
                    
                    if result.get('success'):
                        credentials = result.get('credentials', {})
                        username = credentials.get('username')
                        password = credentials.get('password')
                        security_answer = result.get('security_answer', '')
                        huse_user_id = result.get('data', {}).get('id')
                        
                        print(f"Created new Huse account for {emp.name}")
                        
                        # Update employee status to 3 in Huse
                        if huse_user_id:
                            status_result = huse_update_employee_status(user_id=huse_user_id, status=3)
                            if status_result.get('success'):
                                print(f"Updated Huse status to 3 for {emp.name} (ID: {huse_user_id})")
                            else:
                                print(f"Failed to update Huse status for {emp.name}: {status_result.get('message')}")
                        
                        # Send email with credentials
                        if emp.emailId:
                            email_result = send_huse_credentials_email(
                                employee=emp.name,
                                employee_emails=[emp.emailId],
                                username=username,
                                password=password,
                                security_question=security_question,
                                security_answer=security_answer
                            )
                            if email_result.get('success'):
                                print(f"✅ Email sent to {emp.name} - {email_result.get('message')}")
                            else:
                                print(f"❌ Email failed for {emp.name}: {email_result.get('message')}")
                        
                        # Update database with new credentials
                        EmployeeProxy.update_employee_credentials(emp.id, username, password)
                        print(f"Updated database for {emp.name} with new credentials")
                        
                        # Update the Excel file to mark this employee as registered
                        df.loc[df['ID'] == emp.id, 'Registered'] = "True"
                        df.to_excel(excel_filename, index=False)
                        print(f"Updated Excel file - marked {emp.name} as newly registered")
                        
                    else:
                        error_message = result.get('message', 'Unknown error')
                        print(f"Failed to create new Huse account for {emp.name}: {error_message}")
                        
                        # Extract clean error message from API response
                        error_response = result.get('error', '')
                        if error_response:
                            try:
                                import json
                                error_data = json.loads(error_response)
                                if 'title' in error_data:
                                    clean_error = error_data['title']
                                else:
                                    clean_error = error_response
                            except:
                                clean_error = error_response
                        else:
                            clean_error = error_message
                        
                        # Mark as rejected in Excel with clean error message
                        df.loc[df['ID'] == emp.id, 'Registered'] = f"REJECTED: {clean_error}"
                        df.to_excel(excel_filename, index=False)
                        print(f"Marked {emp.name} as REJECTED in Excel with error: {clean_error}")
                        print("Continuing to next employee...")
                        continue
                    
                    # Continue to next employee after processing existing user
                    continue
            
            print(f"Processing {emp.name} ({emp.emailId})...")
            
            # Check if email or contact already exists in Huse and delete if found
            print(f"Checking for existing users with email '{emp.emailId}' or contact '{emp.contactNo}'...")

            # Find existing user by contact
            existing_contact_id = find_user_id_by_mobile("+" + emp.contactNo)
            if existing_contact_id:
                print(f"Found existing user with contact '{emp.contactNo}' (ID: {existing_contact_id}). Deleting...")
                if delete_user_by_id(existing_contact_id):
                    print(f"✅ Deleted existing user with contact '{emp.contactNo}'")
                else:
                    print(f"❌ Failed to delete existing user with contact '{emp.contactNo}'")
            
            # Find existing user by email
            existing_email_id = find_user_id_by_email(emp.emailId)
            if existing_email_id:
                print(f"Found existing user with email '{emp.emailId}' (ID: {existing_email_id}). Deleting...")
                if delete_user_by_id(existing_email_id):
                    print(f"✅ Deleted existing user with email '{emp.emailId}'")
                else:
                    print(f"❌ Failed to delete existing user with email '{emp.emailId}'")
            
            
            # If no existing users found
            if not existing_email_id and not existing_contact_id:
                print(f"No existing users found with email '{emp.emailId}' or contact '{emp.contactNo}'")
            
            # Prepare employee data
            contact_no = emp.contactNo or ''
            if contact_no and not str(contact_no).startswith('+'):
                contact_no = "+" + str(contact_no)
            
            # Format gender - capitalize first letter, default to "Other" if null
            gender = emp.gender or 'Other'
            if gender and gender.strip():
                gender = gender.strip().capitalize()
            else:
                gender = 'Other'
            
            employee_data = {
                'id': emp.id,
                'name': emp.name,
                'emailId': emp.emailId,
                'contactNo': contact_no,
                'gender': gender,
                'employeeId': emp.employeeId
            }
            
            # Check if employee name is valid
            if not emp.name or emp.name.strip() == '' or emp.name.lower() == 'none':
                print(f"Skipping employee ID {emp.id} - invalid name: '{emp.name}'")
                df.loc[df['ID'] == emp.id, 'Registered'] = "REJECTED: Invalid employee name"
                df.to_excel(excel_filename, index=False)
                continue
            
            # Check if username already exists in Huse
            # First generate the username to check
            first_name, last_name = split_name(emp.name)
            generated_username = generate_username(first_name, last_name)
            
            if check_username_in_huse(generated_username):
                print(f"Username '{generated_username}' already exists in Huse for {emp.name}")
                # Check and update status to 3 for existing user
                users = get_huse_users()
                if users:
                    for user in users:
                        if isinstance(user, dict) and user.get('username') == generated_username:
                            user_id = user.get('id')
                            current_status = user.get('status')
                            if user_id:
                                if current_status != 3:
                                    status_result = huse_update_employee_status(user_id=user_id, status=3)
                                    if status_result.get('success'):
                                        print(f"✅ Updated status from {current_status} to 3 for {emp.name} (ID: {user_id})")
                                    else:
                                        print(f"❌ Failed to update status for {emp.name}: {status_result.get('message')}")
                                else:
                                    print(f"✅ Status is already 3 for {emp.name} - no update needed")
                            break
                
                print(f"Adding existing username to database for {emp.name}")
                
                # Add the existing username to database (no password since user already exists)
                emp.username = generated_username
                emp.password = "EXISTING_USER"  # Mark as existing user
                # Note: This will be committed when the proxy function is called
                print(f"Updated database for {emp.name} with existing username")
                
                # Update Excel file to mark as registered (but with existing username)
                df.loc[df['ID'] == emp.id, 'Registered'] = "True"
                df.to_excel(excel_filename, index=False)
                print(f"Updated Excel file - marked {emp.name} as registered (existing user)")
                continue
            
            # Create Huse credentials
            result = register_employee_in_huse(employee_data)
            
            if result.get('success'):
                credentials = result.get('credentials', {})
                username = credentials.get('username')
                password = credentials.get('password')
                security_answer = result.get('security_answer', '')
                huse_user_id = result.get('data', {}).get('id')
                
                print(f"Created Huse account for {emp.name}")

                # Update employee status to 3 in Huse
                if huse_user_id:
                    status_result = huse_update_employee_status(user_id=huse_user_id, status=3)
                    if status_result.get('success'):
                        print(f"Updated Huse status to 3 for {emp.name} (ID: {huse_user_id})")
                    else:
                        print(f"Failed to update Huse status for {emp.name}: {status_result.get('message')}")
                
                # Send email with credentials
                if emp.emailId:
                    email_result = send_huse_credentials_email(
                        employee=emp.name,
                        employee_emails=[emp.emailId],
                        username=username,
                        password=password,
                        security_question=security_question,
                        security_answer=security_answer
                    )
                    if email_result.get('success'):
                        print(f"✅ Email sent to {emp.name} - {email_result.get('message')}")
                    else:
                        print(f"❌ Email failed for {emp.name}: {email_result.get('message')}")
                
                # Update database with credentials
                EmployeeProxy.update_employee_credentials(emp.id, username, password)
                print(f"Updated database for {emp.name}")
                
                # Update the Excel file to mark this employee as registered
                df.loc[df['ID'] == emp.id, 'Registered'] = "True"
                df.to_excel(excel_filename, index=False)
                print(f"Updated Excel file - marked {emp.name} as registered")
                
            else:
                error_message = result.get('message', 'Unknown error')
                print(f"Failed to create Huse account for {emp.name}: {error_message}")
                
                # Extract clean error message from API response
                error_response = result.get('error', '')
                if error_response:
                    try:
                        import json
                        error_data = json.loads(error_response)
                        if 'title' in error_data:
                            clean_error = error_data['title']
                        else:
                            clean_error = error_response
                    except:
                        clean_error = error_response
                else:
                    clean_error = error_message
                
                # Mark as rejected in Excel with clean error message
                df.loc[df['ID'] == emp.id, 'Registered'] = f"REJECTED: {clean_error}"
                df.to_excel(excel_filename, index=False)
                print(f"Marked {emp.name} as REJECTED in Excel with error: {clean_error}")
                print("Continuing to next employee...")
                continue
    
    except Exception as e:
        print(f"Error: {e}")
    
    # Display summary of skipped employees
    if skipped_no_email:
        print(f"EMPLOYEES SKIPPED DUE TO MISSING EMAIL ADDRESSES")

        print(f"Total skipped: {len(skipped_no_email)}")

        for emp in skipped_no_email:
            print(f"ID: {emp['ID']} | Name: {emp['Name']} | Employee ID: {emp['Employee ID']} | Reason: {emp['Reason']}")
    else:
        print("\nNo employees were skipped due to missing email addresses.")
    
    print("Done")


process_employees()