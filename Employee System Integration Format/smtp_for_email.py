import getpass
import smtplib
import os


# Try these hosts in order:
# HOST = "smtp-mail.outlook.com"  # Standard Outlook
# HOST = "smtp.office365.com"     # Alternative Outlook
# HOST = "smtp.hw.ac.uk"          # University-specific (if exists)
HOST = "mail.huse.ai"
PORT = 465
FROM_EMAIL = "no-reply@huse.ai"
TO_EMAIL = "ahmad04.meda@gmail.com"
PASSWORD = "OLSQBMJPNTSQ4Z7F"

Message = "Hello, this is a test email"

server = smtplib.SMTP(HOST, PORT)
status_code, response = server.ehlo()
print(f"Status code: {status_code}")
print(f"Response: {response}")
status_code, response = server.starttls()
print(f"Status code: {status_code}")
print(f"Response: {response}")
status_code, response = server.login(FROM_EMAIL, PASSWORD)
print(f"Status code: {status_code}")
print(f"Response: {response}")
server.sendmail(FROM_EMAIL, TO_EMAIL, Message)
server.quit()



print("Email sent successfully")