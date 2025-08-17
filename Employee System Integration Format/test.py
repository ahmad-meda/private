User: pls delete employee with the number +971506789012
Entered Soft Delete Employee
Contact Number: 971501234567
HR Database ID: 1
Extraction Messages: [{'role': 'user', 'content': 'pls delete employee with the number +971506789012'}]
Extracted Data: employee_name=None contact_number='+971506789012' email=None
Employee Soft Deleted: 6
User: ashley nicole left the company so pls delete her from the records
Entered Soft Delete Employee
Contact Number: 971501234567
HR Database ID: 1
Extraction Messages: [{'role': 'user', 'content': 'ashley nicole left the company so pls delete her from the records'}]
Extracted Data: employee_name='Ashley Nicole' contact_number=None email=None
Employee Soft Deleted: 8
User: delete matthew andrew taylor
Entered Soft Delete Employee
Contact Number: 971501234567
HR Database ID: 1
Extraction Messages: [{'role': 'user', 'content': 'delete matthew andrew taylor'}]
Extracted Data: employee_name='Matthew Andrew Taylor' contact_number=None email=None
Employee Soft Deleted: 9
User: Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\delete_employee.py", line 88, in <module>
    user_input = input("User: ")
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\delete_employee.py
User: i want to delete Daniel Robert Martinez
Entered Soft Delete Employee
Contact Number: 971501234567
HR Database ID: 1
Extraction Messages: [{'role': 'user', 'content': 'i want to delete Daniel Robert Martinez'}]
Extracted Data: employee_name='Daniel Robert Martinez' contact_number=None email=None
Error: {'message': "Multiple employees found matching 'Daniel Robert Martinez'. Please clarify.present choices to user along with their mentioned details.", 'multiple_employees': [{'name': 'Daniel Robert Martinez', 'email': 'daniel.martinez@distamric.com', 'contactno': '971507890123', 'database_id': 7}, {'name': 'Daniel Robert Martinez', 'email': 'daniel.martinez.dup@distamric.com', 'contactno': '971507890124', 'database_id': 104}]}
Assistant: Hi there! It looks like there are multiple employees with the name 'Daniel Robert Martinez'. Could you kindly provide the contact number or specific details for the correct employee you want to address? Here are the options to clarify:

1. Daniel Robert Martinez, Email: daniel.martinez@distamric.com, Contact Number: 971507890123
2. Daniel Robert Martinez, Email: daniel.martinez.dup@distamric.com, Contact Number: 971507890124

Once you provide more details, I'll be able to assist you further!
User: i choose the second employee
Entered Soft Delete Employee
Contact Number: 971501234567
HR Database ID: 1
Extraction Messages: [{'role': 'user', 'content': 'i want to delete Daniel Robert Martinez'}, {'role': 'assistant', 'content': "Hi there! It looks like there are multiple employees with the name 'Daniel Robert Martinez'. Could you kindly provide the contact number or specific details for the correct employee you want to address? Here are the options to clarify:\n\n1. Daniel Robert Martinez, Email: daniel.martinez@distamric.com, Contact Number: 971507890123\n2. Daniel Robert Martinez, Email: daniel.martinez.dup@distamric.com, Contact Number: 971507890124\n\nOnce you provide more details, I'll be able to assist you further!"}, {'role': 'user', 'content': 'i choose the second employee'}]
Extracted Data: employee_name='Daniel Robert Martinez' contact_number='971507890124' email='daniel.martinez.dup@distamric.com'
Error: {'message': "Multiple employees found matching 'Daniel Robert Martinez'. Please clarify.present choices to user along with their mentioned details.", 'multiple_employees': [{'name': 'Daniel Robert Martinez', 'email': 'daniel.martinez@distamric.com', 'contactno': '971507890123', 'database_id': 7}, {'name': 'Daniel Robert Martinez', 'email': 'daniel.martinez.dup@distamric.com', 'contactno': '971507890124', 'database_id': 104}]}
Employee Soft Deleted: 104
User: PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\delete_employee.py
Entered Soft Delete Employee
Contact Number: 971501234567
HR Database ID: 1
Extraction Messages: [{'role': 'user', 'content': 'PS C:\\Users\\Ahmad Meda\\Desktop\\private-main\\private-main\\Employee System Integration Format> python .\\delete_employee.py'}]
Extracted Data: employee_name=None contact_number=None email=None
Assistant: Hey! Could you please provide either the name or phone number of the employee you wish to delete? Thanks a bunch!
User: User: i want to delete Daniel Robert Martinez
Entered Soft Delete Employee
Contact Number: 971501234567
HR Database ID: 1
Extraction Messages: [{'role': 'user', 'content': 'PS C:\\Users\\Ahmad Meda\\Desktop\\private-main\\private-main\\Employee System Integration Format> python .\\delete_employee.py'}, {'role': 'assistant', 'content': 'Hey! Could you please provide either the name or phone number of the employee you wish to delete? Thanks a bunch!'}, {'role': 'user', 'content': 'User: i want to delete Daniel Robert Martinez'}]
Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\delete_employee.py", line 89, in <module>
    soft_delete_employee(contact_number="+971501234567", user_message=user_input)
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\delete_employee.py", line 42, in soft_delete_employee
    extracted_data = soft_delete_employee_extraction(messages=session_messages[-2:])
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\Utils\agents.py", line 125, in soft_delete_employee_extraction
    completion = client.beta.chat.completions.parse(
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\openai\resources\beta\chat\completions.py", line 116, in parse
    raw_completion = self._client.chat.completions.create(
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\openai\_utils\_utils.py", line 274, in wrapper
    return func(*args, **kwargs)
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\openai\resources\chat\completions.py", line 704, in create
    return self._post(
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\openai\_base_client.py", line 1268, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\openai\_base_client.py", line 945, in request
    return self._request(
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\openai\_base_client.py", line 981, in _request
    response = self._client.send(
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\httpx\_client.py", line 914, in send
    response = self._send_handling_auth(
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\httpx\_client.py", line 942, in _send_handling_auth
    response = self._send_handling_redirects(
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\httpx\_client.py", line 979, in _send_handling_redirects
    response = self._send_single_request(request)
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\httpx\_client.py", line 1015, in _send_single_request
    response = transport.handle_request(request)
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\httpx\_transports\default.py", line 233, in handle_request
    resp = self._pool.handle_request(req)
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\httpcore\_sync\connection_pool.py", line 216, in handle_request
    raise exc from None
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\httpcore\_sync\connection_pool.py", line 196, in handle_request
    response = connection.handle_request(
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\httpcore\_sync\connection.py", line 101, in handle_request
    return self._connection.handle_request(request)
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\httpcore\_sync\http11.py", line 143, in handle_request
    raise exc
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\httpcore\_sync\http11.py", line 113, in handle_request
    ) = self._receive_response_headers(**kwargs)
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\httpcore\_sync\http11.py", line 186, in _receive_response_headers
    event = self._receive_event(timeout=timeout)
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\httpcore\_sync\http11.py", line 224, in _receive_event
    data = self._network_stream.read(
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\site-packages\httpcore\_backends\sync.py", line 126, in read
    return self._sock.recv(max_bytes)
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\ssl.py", line 1226, in recv
    return self.read(buflen)
  File "C:\Users\Ahmad Meda\AppData\Local\Programs\Python\Python39\lib\ssl.py", line 1101, in read
    return self._sslobj.read(len)
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\delete_employee.py
User: Daniel Robert Martinez , pls delete him
Entered Soft Delete Employee
Contact Number: 971501234567
HR Database ID: 1
Extraction Messages: [{'role': 'user', 'content': 'PS C:\\Users\\Ahmad Meda\\Desktop\\private-main\\private-main\\Employee System Integration Format> python .\\delete_employee.py'}, {'role': 'assistant', 'content': 'Hey! Could you please provide either the name or phone number of the employee you wish to delete? Thanks a bunch!'}, {'role': 'user', 'content': 'User: i want to delete Daniel Robert Martinez'}, {'role': 'user', 'content': 'Daniel Robert Martinez , pls delete him'}] 
Extracted Data: employee_name='Daniel Robert Martinez' contact_number=None email=None
Error: {'message': "Multiple employees found matching 'Daniel Robert Martinez'. Please clarify.present choices to user along with their mentioned details.", 'multiple_employees': [{'name': 'Daniel Robert Martinez', 'email': 'daniel.martinez@distamric.com', 'contactno': '971507890123', 'database_id': 7}, {'name': 'Daniel Robert Martinez', 'email': 'daniel.martinez.dup@distamric.com', 'contactno': '971507890124', 'database_id': 104}]}
Assistant: Hi there! I see that you're trying to delete an employee named Daniel Robert Martinez, but there are multiple people with that name in our records. Could you please provide either the phone number or any other distinguishing detail to specify the correct individual? Here are the options:

1. Name: Daniel Robert Martinez
   Email: daniel.martinez@distamric.com
   Contact Number: 971507890123

2. Name: Daniel Robert Martinez
   Email: daniel.martinez.dup@distamric.com
   Contact Number: 971507890124

Let me know which one is the right person to proceed. Thanks!
User: i choose the employee with the email daniel.martinez.dup@distamric.com
Entered Soft Delete Employee
Contact Number: 971501234567
HR Database ID: 1
Extraction Messages: [{'role': 'user', 'content': 'PS C:\\Users\\Ahmad Meda\\Desktop\\private-main\\private-main\\Employee System Integration Format> python .\\delete_employee.py'}, {'role': 'assistant', 'content': 'Hey! Could you please provide either the name or phone number of the employee you wish to delete? Thanks a bunch!'}, {'role': 'user', 'content': 'User: i want to delete Daniel Robert Martinez'}, {'role': 'user', 'content': 'Daniel Robert Martinez , pls delete him'}, {'role': 'assistant', 'content': "Hi there! I see that you're trying to delete an employee named Daniel Robert Martinez, but there are multiple people with that name in our records. Could you please provide either the phone number or any other distinguishing detail to specify the correct individual? Here are the options:\n\n1. Name: Daniel Robert Martinez\n   Email: daniel.martinez@distamric.com\n   Contact Number: 971507890123\n\n2. Name: Daniel Robert Martinez\n   Email: daniel.martinez.dup@distamric.com\n   Contact Number: 971507890124\n\nLet me know which one is the right person to proceed. Thanks!"}, {'role': 'user', 'content': 'i choose the employee with the email daniel.martinez.dup@distamric.com'}]
Extracted Data: employee_name='Daniel Robert Martinez' contact_number='971507890124' email='daniel.martinez.dup@distamric.com'
Error: {'message': "Multiple employees found matching 'Daniel Robert Martinez'. Please clarify.present choices to user along with their mentioned details.", 'multiple_employees': [{'name': 'Daniel Robert Martinez', 'email': 'daniel.martinez@distamric.com', 'contactno': '971507890123', 'database_id': 7}, {'name': 'Daniel Robert Martinez', 'email': 'daniel.martinez.dup@distamric.com', 'contactno': '971507890124', 'database_id': 104}]}
Employee Soft Deleted: 104
User: Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\delete_employee.py", line 88, in <module>
    user_input = input("User: ")
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py:125: SyntaxWarning: "is" with a literal. Did you mean "=="?
  if extracted_data.office_location_name is "manager_skip":
User: Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 238, in <module>
    user_input = input("User: ")
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: hi, pls skip the office location since the new employee is a manager
Entered Create Employee
Contact Number: 971502345678
Session Fields: []
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['full_name', 'contact_number', 'company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender', 'emailId']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name='manager_skip' company_name=None role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {'office_location_name': 'manager_skip'}
in if loop after extraction
{'office_location_name': 'manager_skip'}
Error Dict: {'office_location_name': 'Office location not found,Please clarify.present choices to user. here are the options: Dubai Main Office, Abu Dhabi Branch, Sharjah Office, Ajman Branch, Fujairah Office, Ras Al Khaimah Branch, Al Ain Office, Dubai Media City, Dubai Internet City, DIFC Office, Business Bay Branch, Downtown Dubai Office, Deira Office, Bur Dubai Branch, Jumeirah Office, Marina Branch, Silicon Oasis Office, International City Branch, Dragon Mart Office, Karama Branch'}
Session Fields: ['office_location_name']
Error Dict: {'office_location_name': 'Office location not found,Please clarify.present choices to user. here are the options: Dubai Main Office, Abu Dhabi Branch, Sharjah Office, Ajman Branch, Fujairah Office, Ras Al Khaimah Branch, Al Ain Office, Dubai Media City, Dubai Internet City, DIFC Office, Business Bay Branch, Downtown Dubai Office, Deira Office, Bur Dubai Branch, Jumeirah Office, Marina Branch, Silicon Oasis Office, International City Branch, Dragon Mart Office, Karama Branch'}
Extraction Messages: [{'role': 'user', 'content': 'hi, pls skip the office location since the new employee is a manager'}, {'role': 'user', 'content': 'hi, pls skip the office location since the new employee is a manager'}]
Remaining Fields: ['full_name', 'contact_number', 'company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender', 'emailId']
Explanations: {}
Assistant: Hey there! 😊 To get started with adding the new employee, could you please help me out with some details? We're missing the following info:

- Full Name
- Contact Number
- Company Name
- Role
- Reporting Manager's Name
- Designation
- Date of Joining
- Date of Birth
- Gender
- Email ID

Also, it seems there's a little hiccup with the office location you've mentioned. Could you please confirm from the following options: Dubai Main Office, Abu Dhabi Branch, Sharjah Office, Ajman Branch, Fujairah Office, Ras Al Khaimah Branch, Al Ain Office, Dubai Media City, Dubai Internet City, DIFC Office, Business Bay Branch, Downtown Dubai Office, Deira Office, Bur Dubai Branch, Jumeirah Office, Marina Branch, Silicon Oasis Office, International City Branch, Dragon Mart Office, Karama Branch?

Thanks a ton! Let me know if you need any help with filling these out. 😊
User: the name is Leo Oreo
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['full_name', 'contact_number', 'company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender', 'emailId']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name='Leo Oreo' contact_number=None first_name='Leo' last_name='Oreo' middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {'full_name': 'Leo Oreo', 'first_name': 'Leo', 'last_name': 'Oreo'}
in if loop after extraction
{'full_name': 'Leo Oreo', 'first_name': 'Leo', 'last_name': 'Oreo'}
Error Dict: {}
Session Fields: ['office_location_name']
Error Dict: {}
Extraction Messages: [{'role': 'user', 'content': 'the name is Leo Oreo'}, {'role': 'user', 'content': 'the name is Leo Oreo'}]
Remaining Fields: ['contact_number', 'company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender', 'emailId']       
Explanations: {}
Assistant: Hey there! 😊 I hope you're having a great day! I'm just going through the employee details, and it seems we're missing a few pieces of information to complete this. Could you help me fill in the blanks? I'll need the employee's contact number, company name, role, reporting manager's name, designation, date of joining, date of birth, gender, and email ID. Once we have those, we'll be all set! Thank you so much for your help!
User: the email is leooo@gmail.com and +971509565347 and his company is s3tel incorporated
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['contact_number', 'company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender', 'emailId']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number='+971509565347' first_name=None last_name=None middle_name=None emailId='leooo@gmail.com' designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='S3tel Incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None    
If any data has been extracted from the user message {'contact_number': '+971509565347', 'emailId': 'leooo@gmail.com', 'company_name': 'S3tel Incorporated'}
in if loop after extraction
{'contact_number': '+971509565347', 'emailId': 'leooo@gmail.com', 'company_name': 'S3tel Incorporated'}
Main Fields: ['contact_number', 'company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender', 'emailId']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number='+971509565347' first_name=None last_name=None middle_name=None emailId='leooo@gmail.com' designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='S3tel Incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None    
If any data has been extracted from the user message {'contact_number': '+971509565347', 'emailId': 'leooo@gmail.com', 'company_name': 'S3tel Incorporated'}     
in if loop after extraction
{'contact_number': '+971509565347', 'emailId': 'leooo@gmail.com', 'company_name': 'S3tel Incorporated'}
Optional Location Fields: []
Extracted Data: full_name=None contact_number='+971509565347' first_name=None last_name=None middle_name=None emailId='leooo@gmail.com' designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='S3tel Incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None    
If any data has been extracted from the user message {'contact_number': '+971509565347', 'emailId': 'leooo@gmail.com', 'company_name': 'S3tel Incorporated'}     
in if loop after extraction
{'contact_number': '+971509565347', 'emailId': 'leooo@gmail.com', 'company_name': 'S3tel Incorporated'}
If any data has been extracted from the user message {'contact_number': '+971509565347', 'emailId': 'leooo@gmail.com', 'company_name': 'S3tel Incorporated'}     
in if loop after extraction
{'contact_number': '+971509565347', 'emailId': 'leooo@gmail.com', 'company_name': 'S3tel Incorporated'}
in if loop after extraction
{'contact_number': '+971509565347', 'emailId': 'leooo@gmail.com', 'company_name': 'S3tel Incorporated'}
{'contact_number': '+971509565347', 'emailId': 'leooo@gmail.com', 'company_name': 'S3tel Incorporated'}
Existing Contact: None
AE
Error Dict: {'company_name': 'Company not found'}
Session Fields: ['office_location_name']
Error Dict: {'company_name': 'Company not found'}
Extraction Messages: [{'role': 'user', 'content': 'the email is leooo@gmail.com and +971509565347 and his company is s3tel incorporated'}, {'role': 'user', 'content': 'the email is leooo@gmail.com and +971509565347 and his company is s3tel incorporated'}]
Extraction Messages: [{'role': 'user', 'content': 'the email is leooo@gmail.com and +971509565347 and his company is s3tel incorporated'}, {'role': 'user', 'content': 'the email is leooo@gmail.com and +971509565347 and his company is s3tel incorporated'}]
ent': 'the email is leooo@gmail.com and +971509565347 and his company is s3tel incorporated'}]
Remaining Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hi there! 😊 I just noticed a few details are missing or need correcting in the employee's record. Could you please provide:

- Company Name: It looks like the company is not listed. 🤔
- Role
- Reporting Manager's Name
- Designation
- Date of Joining
- Date of Birth
- Gender

Once we have these, I'll be able to update everything smoothly. Thanks a bunch for your help! 💼🚀
User: Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 238, in <module>
    user_input = input("User: ")
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: company is s3tel incorporated
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='S3tel Incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {'company_name': 'S3tel Incorporated'}
in if loop after extraction
{'company_name': 'S3tel Incorporated'}
Error Dict: {'company_name': 'Company not found'}
Session Fields: ['office_location_name']
Error Dict: {'company_name': 'Company not found'}
Extraction Messages: [{'role': 'user', 'content': 'company is s3tel incorporated'}, {'role': 'user', 'content': 'company is s3tel incorporated'}]
Remaining Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hey there! 😊 Hope you're doing great. Just wanted to let you know that some details are missing or incorrect for the new employee. We need the following info:

- **Company Name:** It seems we're having trouble retrieving this. Could you please confirm the exact company name?
- **Role**
- **Reporting Manager's Name**
- **Designation**
- **Date of Joining**
- **Date of Birth**
- **Gender**

Once we have these, we'll be all set! Thanks a bunch! 💼🙌
User: Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 238, in <module>
    user_input = input("User: ")
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: hi, the company for the new employee is s3tel incorporated
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='S3tel Incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {'company_name': 'S3tel Incorporated'}
in if loop after extraction
{'company_name': 'S3tel Incorporated'}
Error Dict: {'company_name': 'Company not found'}
Session Fields: ['office_location_name']
Error Dict: {'company_name': 'Company not found'}
Extraction Messages: [{'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}, {'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}]
Remaining Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hey there! 😊

I've got a quick update for you. We're missing a few key details for adding the new employee. Could you please provide:
- **Company Name** (currently showing as 'Company not found')
- **Role**
- **Reporting Manager's Name**
- **Designation**
- **Date of Joining**
- **Date of Birth**
- **Gender**

Thanks for helping us get them all set up! 😊
User: Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 238, in <module>
    user_input = input("User: ")
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> 
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: add the new employee to the company s3tel incorporated
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='S3tel Incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {'company_name': 'S3tel Incorporated'}
in if loop after extraction
{'company_name': 'S3tel Incorporated'}
Error Dict: {'company_name': 'Company not found, '}
Session Fields: ['office_location_name']
Error Dict: {'company_name': 'Company not found, '}
Extraction Messages: [{'role': 'user', 'content': 'add the new employee to the company s3tel incorporated'}, {'role': 'user', 'content': 'add the new employee to the company s3tel incorporated'}]
Remaining Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hey there! 😊

Thanks for sending over the details! It looks like we have a few gaps we need to fill in order to add your colleague to our system:

1. **Company Name**: Could you please confirm the name of their company? At the moment, it's showing as 'Company not found'.
2. **Role**: What's their current role?
3. **Reporting Manager's Name**: Who do they report to?
4. **Designation**: What's their official designation?
5. **Date of Joining**: When did they start?
6. **Date of Birth**: Could you share their birth date?
7. **Gender**: How do they identify?

If you could provide these details, we'll be able to get everything up to speed! Thanks a bunch! 😊
User: Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 238, in <module>
    user_input = input("User: ")
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\test.py           
Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\test.py", line 5, in <module>
    print(EmployeeService.get_company_choices(db_session=None, group_id=2))
TypeError: get_company_choices() got an unexpected keyword argument 'db_session'
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\test.py
Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\test.py", line 3, in <module>
    from services.service import EmployeeProxy
ImportError: cannot import name 'EmployeeProxy' from 'services.service' (C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\services\service.py)
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: hi, the company for the new employee is s3tel incorporated
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='S3tel Incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {'company_name': 'S3tel Incorporated'}
in if loop after extraction
{'company_name': 'S3tel Incorporated'}
Error Dict: {'company_name': 'Company not found, '}
Session Fields: ['office_location_name']
Error Dict: {'company_name': 'Company not found, '}
Extraction Messages: [{'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}, {'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}]
Remaining Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hey! 😊 I hope you're doing great. Just wanted to quickly circle back about the new employee you mentioned. 

There are a few details we need to set them up properly:

1. **Company Name** - It seems like the company wasn't recognized. Could you please confirm which company they're joining?
2. **Role** - What's the position they'll be filling?
3. **Reporting Manager Name** - Who will they be reporting to?
4. **Designation** - Can you specify the exact title or designation?
5. **Date of Joining** - When are they starting?
6. **Date of Birth** - Could you share their DOB?
7. **Gender** - Need to update our records for this too.

Once we've got these, we'll be all set! Thanks a ton! 🙌
User: Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 238, in <module>
    user_input = input("User: ")
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: hi, the company for the new employee is s3tel incorporated
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='S3tel Incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {'company_name': 'S3tel Incorporated'}
in if loop after extraction
{'company_name': 'S3tel Incorporated'}
Error Dict: {'company_name': 'Company not found, '}
Session Fields: ['office_location_name']
Error Dict: {'company_name': 'Company not found, '}
Extraction Messages: [{'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}, {'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}]
Remaining Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hey there! 😊 I hope you're having a great day! I noticed we need some more information to get our new employee all set up in the system:

- **Company Name:** It seems like we're missing this one. Could you check and let me know?
- **Role:** What's the role they're stepping into?
- **Reporting Manager Name:** Could you share who they will be reporting to?
- **Designation:** Just need to confirm their official title!
- **Date of Joining:** When is their first day?
- **Date of Birth:** What is the birth date?
- **Gender:** Could you specify this too?

Once we have these details, everything will be good to go! 🚀 Let me know if you have any questions. Thanks a bunch! 🌟
User: Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 238, in <module>
    user_input = input("User: ")
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: hi, the company for the new employee is s3tel incorporated
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='S3tel Incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {'company_name': 'S3tel Incorporated'}
in if loop after extraction
{'company_name': 'S3tel Incorporated'}
Error Dict: {'general': "An unexpected error occurred: local variable 'group_id' referenced before assignment"}
Session Fields: ['office_location_name']
Error Dict: {'general': "An unexpected error occurred: local variable 'group_id' referenced before assignment"}
Extraction Messages: [{'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}, {'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}]
Remaining Fields: ['role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hey there! 😊 It looks like we need a couple more details to get everything sorted.

Could you please check on the following for our new team member? We need the role, reporting manager's name, designation, date of joining, date of birth, and gender.

Also, there's a little hiccup on our end - something about a 'group_id' not being assigned. Don't worry, it's not your fault, just a heads up in case you see anything weird.

Thanks a bunch! Let me know if you need any help with this. 😊
User: Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 238, in <module>
    user_input = input("User: ")
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: hi, the company for the new employee is s3tel incorporated
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='s3tel incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {'company_name': 's3tel incorporated'}
in if loop after extraction
{'company_name': 's3tel incorporated'}
Error Dict: {'company_name': 'Company not found, please clarify. present choices to user. here are the options: Dynasoft Applied System Technology Limited, Cyborg Systems and Solutions'}
Session Fields: ['office_location_name']
Error Dict: {'company_name': 'Company not found, please clarify. present choices to user. here are the options: Dynasoft Applied System Technology Limited, Cyborg Systems and Solutions'}
Extraction Messages: [{'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}, {'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}]
Remaining Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hey there! 😊 It looks like we're missing a few details for the new employee's profile. Could you please provide the following info so we can sort it in if loop after extraction
{'company_name': 's3tel incorporated'}
Error Dict: {'company_name': 'Company not found, please clarify. present choices to user. here are the options: Dynasoft Applied System Technology Limited, Cyborg Systems and Solutions'}
Session Fields: ['office_location_name']
Error Dict: {'company_name': 'Company not found, please clarify. present choices to user. here are the options: Dynasoft Applied System Technology Limited, Cyborg Systems and Solutions'}
Extraction Messages: [{'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}, {'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}]
Remaining Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hey there! 😊 It looks like we're missing a few details for the new employee's profile. Could you please provide the following info so we can sort it g Systems and Solutions'}
Session Fields: ['office_location_name']
Error Dict: {'company_name': 'Company not found, please clarify. present choices to user. here are the options: Dynasoft Applied System Technology Limited, Cyborg Systems and Solutions'}
Extraction Messages: [{'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}, {'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}]
Remaining Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hey there! 😊 It looks like we're missing a few details for the new employee's profile. Could you please provide the following info so we can sort it g Systems and Solutions'}
Extraction Messages: [{'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}, {'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}]
Remaining Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hey there! 😊 It looks like we're missing a few details for the new employee's profile. Could you please provide the following info so we can sort it  the new employee is s3tel incorporated'}]
Remaining Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hey there! 😊 It looks like we're missing a few details for the new employee's profile. Could you please provide the following info so we can sort it Explanations: {}
Assistant: Hey there! 😊 It looks like we're missing a few details for the new employee's profile. Could you please provide the following info so we can sort it Assistant: Hey there! 😊 It looks like we're missing a few details for the new employee's profile. Could you please provide the following info so we can sort it out?

1. **Company Name**: Seems like we're missing this. Could you pick from these options: Dynasoft Applied System Technology Limited, Cyborg Systems and Solutions? 
2. **Role**: What's the position they'll be holding?
3. **Reporting Manager's Name**: Who will they report to?
4. **Designation**: Could you clarify the designation?
5. **Date of Joining**: When did they start or plan to start?
6. **Date of Birth**: We need their birthdate.
7. **Gender**: And lastly, what's their gender?

Once we have this info, we're good to go! Thanks a ton for your help! 🌟
User: Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 238, in <module>
    user_input = input("User: ")
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: hi, the company for the new employee is s3tel incorporated
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='S3tel Incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 239, in <module>
    create_employee(contact_number="+971502345678", user_message=user_input)
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 88, in create_employee
    extracted_data.company_name = find_best_match(user_input=extracted_data.company_name, choices=EmployeeChoices.get_companies_choices(group_id=employee_record.group_id), threshold=85)
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\Utils\choices.py", line 15, in get_companies_choices
    return EmployeeProxy.get_company_choices(group_id)
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\proxies\proxy.py", line 52, in get_company_choices
    return EmployeeService.get_company_choices(db.session, group_id)
TypeError: get_company_choices() missing 1 required positional argument: 'company_id'
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: hi, the company for the new employee is s3tel incorporated
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='s3tel incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 239, in <module>
    create_employee(contact_number="+971502345678", user_message=user_input)
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 88, in create_employee
    extracted_data.company_name = find_best_match(user_input=extracted_data.company_name, choices=EmployeeChoices.get_companies_choices(group_id=employee_record.group_id, company_id=employee_record.company_id), threshold=85)
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\Utils\choices.py", line 15, in get_companies_choices
    return EmployeeProxy.get_company_choices(group_id, company_id)
TypeError: get_company_choices() takes 1 positional argument but 2 were given
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: hi, the company for the new employee is s3tel incorporated
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='s3tel incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 239, in <module>
    create_employee(contact_number="+971502345678", user_message=user_input)
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 88, in create_employee
    extracted_data.company_name = find_best_match(user_input=extracted_data.company_name, choices=EmployeeChoices.get_companies_choices(group_id=employee_record.group_id, company_id=employee_record.company_id), threshold=85)
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\Utils\choices.py", line 15, in get_companies_choices
    return EmployeeProxy.get_company_choices(group_id, company_id)
TypeError: get_company_choices() takes 1 positional argument but 2 were given
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: hi, the company for the new employee is s3tel incorporated
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='S3tel Incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {'company_name': 'S3tel Incorporated'}
in if loop after extraction
{'company_name': 'S3tel Incorporated'}
Error Dict: {'company_name': 'Company not found, please clarify. present choices to user. here are the options: '}
Session Fields: ['office_location_name']
Error Dict: {'company_name': 'Company not found, please clarify. present choices to user. here are the options: '}
Extraction Messages: [{'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}, {'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}]
Remaining Fields: ['company_name', 'role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hey there! 😊 Just a quick check-in about the employee details.

It seems like we're missing or need clarification on a few key points:

- **Company Name**: It looks like there’s been a mix-up. Could you confirm which company they will be working for? Here are the options we have: [Insert company options here].
- **Role**: Could you specify the role they'll be filling?
- **Reporting Manager's Name**: We'll need to know who they'll be reporting to.
- **Designation**: What's their official title?
- **Date of Joining**: When are they starting with us?
- **Date of Birth**: Could you provide their birthdate?
- **Gender**: What gender should we list for them?

Thanks a bunch! Once we have these details, we can get them all set up. 😊
User: Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 238, in <module>
    user_input = input("User: ")
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> 
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: hi, the company for the new employee is s3tel incorporated
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 None
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name='S3tel Incorporated' role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {'company_name': 'S3tel Incorporated'}
in if loop after extraction
{'company_name': 'S3tel Incorporated'}
Error Dict: {'company_name': 'Company not found, please clarify. present choices to user. here are the options: Dynasoft Applied System Technology Limited'}
Session Fields: ['office_location_name']
Error Dict: {'company_name': 'Company not found, please clarify. present choices to user. here are the options: Dynasoft Applied System Technology Limited'}
Extraction Messages: [{'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}, {'role': 'user', 'content': 'hi, the company for the new employee is s3tel incorporated'}]
Remaining Fields: ['role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Explanations: {}
Assistant: Hey there! 😊 Could you help me fill in a few details for adding the new team member? We're missing or have incorrect info for the following:

- Role
- Reporting Manager's Name
- Designation
- Date of Joining
- Date of Birth
- Gender

Also, I noticed there's an issue with the company name. Could you confirm if it's 'Dynasoft Applied System Technology Limited'? 👀

Thanks a ton!
User: gender is male and he joined us on 2024 3rd may and his dob is 3rd october 2003 and his designation is Ai Engineer, reporting manager is John Michael Smith

Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['role', 'reporting_manager_name', 'designation', 'dateOfJoining', 'dateOfBirth', 'gender']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation='Ai Engineer' dateOfJoining='2024-05-03' dateOfBirth='2003-10-03' gender='male' work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role=None reporting_manager_name='John Michael Smith' department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None 
If any data has been extracted from the user message {'designation': 'Ai Engineer', 'dateOfJoining': '2024-05-03', 'dateOfBirth': '2003-10-03', 'gender': 'Male', 'reporting_manager_name': 'John Michael Smith'}
in if loop after extraction
{'designation': 'Ai Engineer', 'dateOfJoining': '2024-05-03', 'dateOfBirth': '2003-10-03', 'gender': 'Male', 'reporting_manager_name': 'John Michael Smith'}     
Error Dict: {}
Session Fields: ['office_location_name']
Error Dict: {}
Extraction Messages: [{'role': 'user', 'content': 'gender is male and he joined us on 2024 3rd may and his dob is 3rd october 2003 and his designation is Ai Engineer, reporting manager is John Michael Smith'}, {'role': 'user', 'content': 'gender is male and he joined us on 2024 3rd may and his dob is 3rd october 2003 and his designation is Ai Engineer, reporting manager is John Michael Smith'}]
Remaining Fields: ['role']
Explanations: {}
Assistant: Hey there! 😊 It looks like we're missing a bit of info to complete the employee's profile. Could you let me know what their role is? 🤔 As soon as you provide that, we'll be all set to finalize their details! Thanks a ton! 🌟
User: role is super admin
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['role']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role='super admin' reporting_manager_nam his designation is Ai Engineer, reporting manager is John Michael Smith'}]
Remaining Fields: ['role']
Explanations: {}
Assistant: Hey there! 😊 It looks like we're missing a bit of info to complete the employee's profile. Could you let me know what their role is? 🤔 As soon as you provide that, we'll be all set to finalize their details! Thanks a ton! 🌟
User: role is super admin
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['role']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role='super admin' reporting_manager_namRemaining Fields: ['role']
Explanations: {}
Assistant: Hey there! 😊 It looks like we're missing a bit of info to complete the employee's profile. Could you let me know what their role is? 🤔 As soon as you provide that, we'll be all set to finalize their details! Thanks a ton! 🌟
User: role is super admin
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['role']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role='super admin' reporting_manager_namExplanations: {}
Assistant: Hey there! 😊 It looks like we're missing a bit of info to complete the employee's profile. Could you let me know what their role is? 🤔 As soon as you provide that, we'll be all set to finalize their details! Thanks a ton! 🌟
User: role is super admin
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['role']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role='super admin' reporting_manager_namUser: role is super admin
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['role']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role='super admin' reporting_manager_namEmployee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: ['role']
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role='super admin' reporting_manager_namOptional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role='super admin' reporting_manager_namOptional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role='super admin' reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role='super admin' reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
one gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role='super admin' reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
e=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {'role': 'Super Admin'}
in if loop after extraction
in if loop after extraction
{'role': 'Super Admin'}
Error Dict: {}
Error Dict: {}
Session Fields: ['office_location_name']
Error Dict: {}
Extraction Messages: [{'role': 'user', 'content': 'role is super admin'}, {'role': 'user', 'content': 'role is super admin'}]
Remaining Fields: ['is_hr', 'hr_scope', 'reminders']
Explanations: {}
Assistant: Hey there! Hope you're doing well. 😊

I've got a few things I need some info on to add the employee:

1. **is_hr** - Could you let me know if the employee is part of the HR department?
2. **hr_scope** - What's their level of HR access or responsibility?
3. **reminders** - Will they need any specific reminders set up in the system?

Let me know whenever you have a moment. Thanks a ton! 🙌
User: Traceback (most recent call last):
  File "C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format\create_employee.py", line 238, in <module>
    print(f"Explanations: {explanations}")
KeyboardInterrupt
PS C:\Users\Ahmad Meda\Desktop\private-main\private-main\Employee System Integration Format> python .\create_employee.py
User: hi
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: []
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {}
Session Fields: ['office_location_name']
currently in optional fields
Remaining Fields: ['is_hr', 'hr_scope', 'reminders']
Skipped Fields: None
Error Dict: {}
Extraction Messages: [{'role': 'user', 'content': 'hi'}, {'role': 'user', 'content': 'hi'}]
Remaining Fields: ['is_hr', 'hr_scope', 'reminders']
Explanations: {'reminders': '\n        This reminders is for the employee to get reminders for daily check-in and check-out.\n        Ask the user if this employee needs reminders for daily check-in and check-out.\n        ', 'is_hr': '\n        Ask the user if the employee is an HR.\n        ', 'hr_scope': '\n        Ask the user if the employee is an HR for the group or the company.\n        '}
Assistant: Hey there! I noticed we're missing a few details for your new employee's profile. Could you help me out?

1. Does this employee need reminders for daily check-in and check-out?
2. Is this employee an HR?
3. If so, are they an HR for the group or the entire company?

Let me know so we can get everything set up smoothly. Thanks a bunch! 😊
User: yes he needs reminders and he is an hr and he is an hr for the company
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: []
Optional Personal Fields: ['is_hr', 'hr_scope', 'reminders']
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role=None reporting_manager_name=None department_name=None restrict_to_allowed_locations=None allow_site_checkin=None reminders=True is_hr=True hr_scope='company'
If any data has been extracted from the user message {'reminders': True, 'is_hr': True, 'hr_scope': 'company'}
in if loop after extraction
{'reminders': True, 'is_hr': True, 'hr_scope': 'company'}
Error Dict: {}
Session Fields: ['office_location_name', 'reminders', 'is_hr', 'hr_scope']
Error Dict: {}
Extraction Messages: [{'role': 'user', 'content': 'yes he needs reminders and he is an hr and he is an hr for the company'}, {'role': 'user', 'content': 'yes he needs reminders and he is an hr and he is an hr for the company'}]
Remaining Fields: ['department_name']
Explanations: {}
Assistant: Hey there! 😊 I noticed we're missing the 'department_name' for the new employee. Could you send me that info? Much appreciated! 🌟
User: department is sales  
Entered Create Employee
Contact Number: 971502345678
Session Fields: ['office_location_name', 'reminders', 'is_hr', 'hr_scope']
Employee Record: 1 2
Employee Name: Sarah Elizabeth Johnson
Main Fields: []
Optional Personal Fields: []
Optional Employment Fields: ['department_name', 'office_location_name']
Optional Location Fields: []
Extracted Data: full_name=None contact_number=None first_name=None last_name=None middle_name=None emailId=None designation=None dateOfJoining=None dateOfBirth=None gender=None work_policy_name=None home_latitude=None home_longitude=None office_location_name=None company_name=None role=None reporting_manager_name=None department_name='Sales' restrict_to_allowed_locations=None allow_site_checkin=None reminders=None is_hr=None hr_scope=None
If any data has been extracted from the user message {'department_name': 'Sales'}
in if loop after extraction
{'department_name': 'Sales'}
Error Dict: {}
Session Fields: ['office_location_name', 'reminders', 'is_hr', 'hr_scope']
Adding in main database
User: 