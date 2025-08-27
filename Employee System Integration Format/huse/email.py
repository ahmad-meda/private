import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from datetime import datetime


def send_huse_credentials_email(employee_email: str, 
                              username: str, 
                              password: str, 
                              security_question: str, 
                              security_answer: str) -> Dict[str, Any]:
    """
    Send email with Huse app credentials to the employee
    
    Args:
        employee_email: Employee's email address
        username: Huse app username
        password: Huse app password
        security_question: Security question for account recovery
        security_answer: Answer to the security question
        
    Returns:
        Dictionary with success status and message
    """
    # Debug: Print what the email function received
    print("Email function received:")
    print(f"employee_email: {employee_email}")
    print(f"username: {username}")
    print(f"password: {password}")
    print(f"security_question: {security_question}")
    print(f"security_answer: {security_answer}")
    print(f"security_answer type: {type(security_answer)}")
    print(f"security_answer length: {len(str(security_answer)) if security_answer else 0}")
    try:
        # Email configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'ahmad04.meda@gmail.com'
        sender_password = 'awkw yern lqnz ptjm'  # Set this in environment variables
        
        if not sender_password:
            return {
                'success': False,
                'message': 'Gmail password not configured. Set GMAIL_PASSWORD environment variable.'
            }
        
        # Create email content
        subject = "Your Huse App Login Credentials"
        
        # Simple HTML email
        html_content = f"""
        <html>
        <body>
            <h2>Your Huse App Credentials</h2>
            
            <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3>Login Information:</h3>
                <p><strong>Username:</strong> {username}</p>
                <p><strong>Password:</strong> {password}</p>
            </div>
            
            <div style="background-color: #e8f4fd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3>Security Information:</h3>
                <p><strong>Security Question:</strong> {security_question}</p>
                <p><strong>Security Answer:</strong> {security_answer}</p>
            </div>
            
            <p>Best regards,<br>HR Team</p>
            <hr>
            <p style="font-size: 12px; color: #666;">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body>
        </html>
        """
        
        # Simple text email
        text_content = f"""
Your Huse App Credentials

Login Information:
Username: {username}
Password: {password}

Security Information:
Security Question: {security_question}
Security Answer: {security_answer}

Best regards,
HR Team

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = employee_email
        msg['Subject'] = subject
        
        # Attach both HTML and text versions
        text_part = MIMEText(text_content, 'plain')
        html_part = MIMEText(html_content, 'html')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return {
            'success': True,
            'message': f'Credentials email sent successfully to {employee_email}'
        }
        
    except smtplib.SMTPAuthenticationError:
        return {
            'success': False,
            'message': 'Email authentication failed. Check Gmail password.'
        }
    except smtplib.SMTPRecipientsRefused:
        return {
            'success': False,
            'message': f'Invalid recipient email: {employee_email}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error sending email: {str(e)}',
            'error': str(e)
        }
