# from huse.credentials import generate_credentials
# from Utils.password_helpers import check_password

# # username, plain_password, encrypted_password = generate_credentials("John Doe")

# # print(username)
# # print(plain_password)
# # print(encrypted_password)

# # username2, plain_password2, encrypted_password2 = generate_credentials("John Doe")
# # print(username2)
# # print(plain_password2)
# # print(encrypted_password2)

# # #  check password 

# # print(check_password(plain_password, encrypted_password))
# # print(check_password(plain_password2, encrypted_password2))

# # Employee record 214 in the main Employee Database

# # Step 1: send api request to huse to register the employee

# from huse.backend import register_employee_in_huse
# from proxies.proxy import EmployeeProxy

# # Get employee record
# employee_obj = EmployeeProxy.get_employee_record_by_id(283)
# print(f"Employee object type: {type(employee_obj)}")
# print(f"Employee object: {employee_obj}")

# # # Convert SQLAlchemy object to dictionary
# employee_data = {
#     'id': employee_obj.id,
#     'name': employee_obj.name+"Eshu",
#     'emailId': "rathwalA292e707@gmail.com",
#     'contactNo': "+" + "971561101062", #+ employee_obj.contactNo,
#     'gender': employee_obj.gender,
#     'designation': employee_obj.designation,
#     'dateOfJoining': employee_obj.dateOfJoining,
#     'dateOfBirth': employee_obj.dateOfBirth,
#     'first_name': employee_obj.first_name,
#     'middle_name': employee_obj.middle_name,
#     'last_name': employee_obj.last_name
# }

# print(f"Employee data dictionary: {employee_data}")# change

# # Test Huse registration
# result = register_employee_in_huse(employee_data)
# print(f"Registration result: {result}")

# # # Step 2: send email to the employee with the credentials
# from huse.email import send_huse_credentials_email

# if result and result.get('success'):
#     # Extract credentials from the response
#     credentials = result.get('credentials', {})
#     huse_data = result.get('data', {})
    
#     # Debug: Print what we're sending to email function
# print("Email parameters:")
# print(f"employee_email: {employee_data.get('emailId')}")
# print(f"username: {credentials.get('username')}")
# print(f"password: {credentials.get('password')}")
# print(f"security_question: {huse_data.get('securityQuestion')}")
# print(f"security_answer: {result.get('security_answer')}")

# List of 3 email addresses to send credentials to
# email_list = [ # Original employee email
#     "ahmad04.meda@gmail.com",              # HR email
#     "am2260@hw.ac.uk",
#     "ylcofficialfactsfix@gmail.com",
#     "ashu4meda@gmail.com",
    
#     # "ruhban13@hotmail.com"        # Admin email
# ]

# from huse.email import send_huse_credentials_email
# print(send_huse_credentials_email(
#     employee="Muhammed Saneer",
#     employee_emails=email_list,
#     username="muhammedsaneer",
#     password="fdjsbh",
#     security_question="What is your favourite colour?",
#     security_answer="Faiyaz"
# ))


import requests

# url = "http://192.168.0.106:5001/crm_to_huse"

# headers = {
    
#     "huse-api-key": "testestesttesing"
# }

# url = "https://fd46a5844900.ngrok.app/crm_to_huse"

# headers = {
#     "huse-api-key": "6rnZ0LVmJ1Lr9_yq9VHTUGXvF4RtTP7k2k95nKxBy6A"
# }

# crm_object =  {'approval_status': 'pending', 'company': None, 'crm_backend_id': '68ca55b3e744f7515', 'date_of_birth': None, 'education_background': None, 'email': 'mera66@gmail.com', 'id_number': None, 'job_title': None, 'lead_comments': None, 'lead_status': 'Hot', 'linkedin_or_website': None, 'name': 'shriraj kamte', 'nationality': 'Aruba', 'notable_affiliations': None, 'occupation': None, 'passport_number': None, 'phone': '+911028625544', 'preferred_nickname': 'shriraj', 'residential_address': None, 'status': 'New', 'suggested_membership_tier': 'The Rufescent Preferred'}
# response = requests.post(url, headers=headers, json=crm_object)
# print(response.json())


# from proxies.proxy import EmployeeProxy

# employees = EmployeeProxy.get_all_active_employees()
# print(employees)

# from proxies.employee_session_proxy import EmployeeSessionProxy

# EmployeeSessionProxy.clear_asked_confirmation(contact_number="+971512345678")
# EmployeeSessionProxy.clear_employee_session(contact_number="+971512345678")
# EmployeeSessionProxy.clear_messages(contact_number="+971512345678")
# EmployeeSessionProxy.clear_user_trying_to_add_new_employee(contact_number="+971512345678")
# EmployeeSessionProxy.clear_asked_user_draft_continuation(contact_number="+971512345678")
# EmployeeSessionProxy.clear_list(contact_number="+971512345678")
# EmployeeSessionProxy.clear_employee_asked_confirmation(contact_number="+971512345678")
# EmployeeSessionProxy.clear_update_agent_confirmation(contact_number="+971512345678")
# EmployeeSessionProxy.clear_user_trying_to_add_new_employee(contact_number="+971512345678")


# from helpers.user_record import update_user_record, get_huse_user_by_username
# print(get_huse_user_by_username(username="nicokidm"))

# print(update_user_record(username="nicokidm",email="nicoletestingkidman@gmail.com"))

# from proxies.proxy import EmployeeProxy
# print(EmployeeProxy.clear_employee_draft_fields(draft_id=307))

# from Utils.extraction_fields import get_filled_fields
# from proxies.proxy import EmployeeProxy
# from proxies.employee_session_proxy import EmployeeSessionProxy

# employee_record = EmployeeProxy.get_employee_draft_record_by_id(317)
# print(get_filled_fields(employee_record))


# print(EmployeeSessionProxy.get_messages(contact_number="+971509784398"))