import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from static.templates.huse_crendentials import huse_credentials_template

load_dotenv()



def send_huse_credentials_email(employee: str,
                                employee_emails: list, 
                                username: str, 
                                password: str, 
                                security_question: str, 
                                security_answer: str) -> Dict[str, Any]:
    """
    Send email with Huse app credentials to multiple employees
    
    Args:
        employee_emails: List of employee email addresses
        username: Huse app username
        password: Huse app password
        security_question: Security question for account recovery
        security_answer: Answer to the security question
        
    Returns:
        Dictionary with success status and message
    """
    # Debug: Print what the email function received
    print("Email function received:")
    print(f"employee_emails: {employee_emails}")
    print(f"username: {username}")
    print(f"password: {password}")
    print(f"security_question: {security_question}")
    print(f"security_answer: {security_answer}")
    print(f"security_answer type: {type(security_answer)}")
    print(f"security_answer length: {len(str(security_answer)) if security_answer else 0}")
    
    # Validate input
    if not employee_emails or not isinstance(employee_emails, list):
        return {
            'success': False,
            'message': 'Invalid input: employee_emails must be a non-empty list'
        }
    
    try:
        
        # Email configuration
        smtp_server = 'mail.huse.ai'
        smtp_port = 587
        sender_email = os.environ.get('EMAIL_SENDER_ADDRESS')
        sender_password = os.environ.get('EMAIL_SENDER_PASSWORD')
        print(f"Sender Email: {sender_email}")
        print(f"Sender Password: {sender_password}")
        
        # Create email content
        subject = f"{employee}'s Huse App Login Credentials"
        
        # Use the template function to generate HTML content
        html_content = huse_credentials_template(subject, employee, username, password, security_question, security_answer)
            
        
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ', '.join(employee_emails)  # Join multiple emails with commas
        msg['Subject'] = subject
        
        # Attach HTML version
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        
        # Send email with validation
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS
            server.login(sender_email, sender_password)
            refused = server.send_message(msg)
            if refused:
                return {'success': False, 'message': f'SMTP refused recipients: {refused}'}
            else:
                print(f"✅ SMTP ACCEPTED - Email queued for delivery to {employee_emails}")
                return {'success': True, 'message': f'SMTP accepted - Email sent to {employee_emails}'}
        
        
    except smtplib.SMTPAuthenticationError:
        return {
            'success': False,
            'message': 'Email authentication failed. Check email password.'
        }
    except smtplib.SMTPRecipientsRefused as e:
        failed_recipients = list(e.recipients.keys())
        return {
            'success': False,
            'message': f'Invalid recipient email(s): {", ".join(failed_recipients)}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error sending email: {str(e)}',
            'error': str(e)
        }