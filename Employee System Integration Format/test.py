from huse.credentials import generate_credentials
from Utils.password_helpers import check_password

# username, plain_password, encrypted_password = generate_credentials("John Doe")

# print(username)
# print(plain_password)
# print(encrypted_password)

# username2, plain_password2, encrypted_password2 = generate_credentials("John Doe")
# print(username2)
# print(plain_password2)
# print(encrypted_password2)

# #  check password 

# print(check_password(plain_password, encrypted_password))
# print(check_password(plain_password2, encrypted_password2))

# Employee record 214 in the main Employee Database

# Step 1: send api request to huse to register the employee

from huse.backend import register_employee_in_huse
from proxies.proxy import EmployeeProxy

# Get employee record
employee_obj = EmployeeProxy.get_employee_record_by_id(283)
print(f"Employee object type: {type(employee_obj)}")
print(f"Employee object: {employee_obj}")

# Convert SQLAlchemy object to dictionary
employee_data = {
    'id': employee_obj.id,
    'name': employee_obj.name,
    'emailId': "am2260@hw.ac.uk",
    'contactNo': "+" + employee_obj.contactNo,
    'gender': employee_obj.gender,
    'designation': employee_obj.designation,
    'dateOfJoining': employee_obj.dateOfJoining,
    'dateOfBirth': employee_obj.dateOfBirth,
    'first_name': employee_obj.first_name,
    'middle_name': employee_obj.middle_name,
    'last_name': employee_obj.last_name
}

print(f"Employee data dictionary: {employee_data}")# change

# Test Huse registration
result = register_employee_in_huse(employee_data)
print(f"Registration result: {result}")

# Step 2: send email to the employee with the credentials
from huse.email import send_huse_credentials_email

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
    
    send_huse_credentials_email(
        employee_email=employee_data.get('emailId'),
        username=credentials.get('username'),
        password=credentials.get('password'),
        security_question=huse_data.get('securityQuestion'),
        security_answer=result.get('security_answer')  # Use locally generated security answer
    )
else:
    print(f"Failed to register employee: {result}")

# Step 3: send email to the hr with the credentials

