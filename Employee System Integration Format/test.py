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

url = "https://app.huse.ai/crm_to_huse"

headers = {
    "huse-api-key": "6rnZ0LVmJ1Lr9_yq9VHTUGXvF4RtTP7k2k95nKxBy6A"
}

crm_object = {'id': '690095337475d3041', 'approval_status': 'pending', 'company': None, 'crm_backend_id': '690095337475d3141', 'date_of_birth': None, 'education_background': None, 'email': 'karandhapate344354@gmail.com', 'id_number': None, 'job_title': None, 'lead_comments': None, 'lead_status': 'Hot', 'linkedin_or_website': None, 'name': 'karandhapate344354@gmail.com', 'nationality': 'Aruba', 'notable_affiliations': None, 'occupation': None, 'passport_number': None, 'phone': '+97189981531', 'preferred_nickname': 'bhdvgwd', 'residential_address': None, 'status': 'New', 'suggested_membership_tier': 'The Rufescent Associate'}
response = requests.post(url, headers=headers, json=crm_object)
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")
print(f"Response Headers: {response.headers}")


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


# EmployeeSessionProxy.clear_asked_confirmation(contact_number="+971509784398")
# EmployeeSessionProxy.clear_employee_session(contact_number="+971509784398")
# EmployeeSessionProxy.clear_messages(contact_number="+971509784398")
# EmployeeSessionProxy.clear_user_trying_to_add_new_employee(contact_number="+971509784398")
# EmployeeSessionProxy.clear_asked_user_draft_continuation(contact_number="+971509784398")
# EmployeeSessionProxy.clear_list(contact_number="+971509784398")
# EmployeeSessionProxy.clear_employee_asked_confirmation(contact_number="+971509784398")
# EmployeeSessionProxy.clear_update_agent_confirmation(contact_number="+971509784398")
# EmployeeSessionProxy.clear_user_trying_to_add_new_employee(contact_number="+971509784398")


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


# from datetime import datetime, timedelta
# from proxies.proxy import EmployeeProxy
# employee_record = EmployeeProxy.get_employee_draft_record_by_id(323)
# current_time = datetime.now()
# record_to_check_time = employee_record.updated_at
# time_difference = current_time - record_to_check_time
# print(f"Time difference: {time_difference}")
# print(timedelta(minutes=30))

# from Utils.choices import EmployeeChoices

# from proxies.employee_choices_proxy import EmployeeChoicesProxy
# print("office location choices",EmployeeChoicesProxy.get_office_location_choices())
# print("company choices",EmployeeChoicesProxy.get_company_choices())
# print("department choices",EmployeeChoicesProxy.get_department_choices())
# print("role choices",EmployeeChoicesProxy.get_role_choices())
# print("gender choices",EmployeeChoicesProxy.get_gender_choices())
# print("work policy choices",EmployeeChoicesProxy.get_work_policy_choices())
# print("group choices",EmployeeChoicesProxy.get_group_choices())


# """You are HUSE, enhanced with retrieval-augmented generation capabilities, 
# at a multinational corporation. Your role involves understanding and processing employee queries 
# about company policies, benefits, leaves, code of conduct, and other HR-related matters. 
# You do this by extracting relevant entities and context from their questions.

# You will adhere to the following guidelines:

# 1/ Generate responses that closely match the style and content of an HR representative.
# 2/ Keep responses concise. If the query is vague like "elaborate", clarify the previous message.
# 3/ Only use information from the knowledge base or context. Never hallucinate.
# 4/ Use the user's past messages (below) for continuity.
# 5/ Do not say you're retrieving from documents — speak as if you're the HR expert.

# Your job is to display the employee details in a friendly, casual way in whatsapp chat.

#         Using supporting knowledge, create a friendly, casual WhatsApp message to the user.

#         If Employee details are present, always treat it as a successful search.

#         If the user has provided any errors, inform them about the errors in a friendly way. This applies only if there are errors present.

#         If you have the information, do not say "I don't have that information" or "I cannot answer that at the moment."

#         Make sure to format the message in a way that is easy to read on WhatsApp, using line breaks and bullet points if necessary."""


# extra = (
#     """ Your job is to provide helpful responses based solely only on the employee information AND user's latest query in a friendly, casual WhatsApp chat format.

#                     The employee details provided are fetched based on the user's query, so use this information to answer in a way that fullfills their latest request in a friendly, casual WhatsApp message.

#                     If Employee details are present, always treat it as a successful search and use that information to provide relevant answers.

#                     If the user has provided any errors, inform them about the errors in a friendly way. This applies only if there are errors present.

#                     If you have the information, do not say "I don't have that information" or "I cannot answer that at the moment."

#                     Make sure to format the message in a way that is easy to read on WhatsApp, using line breaks and bullet points if necessary."""
# )


# errors = {
    
# }


# from helpers.user_record import get_huse_user_by_username, update_user_record

# print(get_huse_user_by_username(username="batckinm"))

# print(update_user_record(username="batckinm",email="batckingmeistertesting@gmail.com"))