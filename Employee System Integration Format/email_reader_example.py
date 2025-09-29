#!/usr/bin/env python3
"""
Example of reading emails from inbox using different methods.
"""

import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

load_dotenv()

def read_emails_imap(email_address, password, server="imap.gmail.com", port=993):
    """
    Read emails using IMAP (most common method).
    
    Args:
        email_address: Your email address
        password: Your email password (or app password for Gmail)
        server: IMAP server (default: Gmail)
        port: IMAP port (default: 993 for SSL)
    """
    try:
        # Connect to server
        mail = imaplib.IMAP4_SSL(server, port)
        mail.login(email_address, password)
        
        # Select inbox
        mail.select("inbox")
        
        # Search for emails (all emails)
        status, messages = mail.search(None, "ALL")
        
        # Get email IDs
        email_ids = messages[0].split()
        
        # Get last 10 emails
        latest_emails = email_ids[-10:] if len(email_ids) >= 10 else email_ids
        
        emails = []
        
        for email_id in latest_emails:
            # Fetch email
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
            # Parse email
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            # Extract information
            subject = decode_header(email_message["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            
            sender = decode_header(email_message["From"])[0][0]
            if isinstance(sender, bytes):
                sender = sender.decode()
            
            date = email_message["Date"]
            
            # Check if read/unread
            status_flags = email_message.get("X-GM-LABELS", "")
            is_read = "\\Seen" in str(status_flags)
            
            # Get email body
            body = ""
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = email_message.get_payload(decode=True).decode()
            
            emails.append({
                "id": email_id.decode(),
                "subject": subject,
                "sender": sender,
                "date": date,
                "is_read": is_read,
                "body": body[:200] + "..." if len(body) > 200 else body
            })
        
        mail.close()
        mail.logout()
        
        return emails
        
    except Exception as e:
        print(f"Error reading emails: {str(e)}")
        return []

def read_emails_simple():
    """
    Simple example using environment variables.
    """
    email_address = os.environ.get('EMAIL_SENDER_ADDRESS')
    email_password = os.environ.get('EMAIL_SENDER_PASSWORD')
    
    if not email_address or not email_password:
        print("Please set EMAIL_SENDER_ADDRESS and EMAIL_SENDER_PASSWORD in your .env file")
        return []
    
    print(f"Reading emails for: {email_address}")
    emails = read_emails_imap(email_address, email_password)
    
    return emails

def display_emails(emails):
    """
    Display emails in a nice format.
    """
    print(f"\n{'='*80}")
    print(f"FOUND {len(emails)} EMAILS")
    print(f"{'='*80}")
    
    for i, email in enumerate(emails, 1):
        status = "📖 READ" if email['is_read'] else "📧 UNREAD"
        print(f"\n{i}. {status}")
        print(f"   From: {email['sender']}")
        print(f"   Subject: {email['subject']}")
        print(f"   Date: {email['date']}")
        print(f"   Body: {email['body']}")
        print(f"   {'-'*60}")

if __name__ == "__main__":
    print("EMAIL READER EXAMPLE")
    print("=" * 50)
    
    # Read emails
    emails = read_emails_simple()
    
    if emails:
        display_emails(emails)
    else:
        print("No emails found or error occurred")
    
    print(f"\n{'='*80}")
    print("USAGE INSTRUCTIONS:")
    print(f"{'='*80}")
    print("""
1. For Gmail:
   - Enable 2-factor authentication
   - Generate an "App Password" 
   - Use the app password instead of your regular password

2. For other email providers:
   - Gmail: imap.gmail.com:993
   - Outlook: outlook.office365.com:993
   - Yahoo: imap.mail.yahoo.com:993

3. Set environment variables in .env file:
   EMAIL_SENDER_ADDRESS=your-email@gmail.com
   EMAIL_SENDER_PASSWORD=your-app-password

4. The function returns a list of dictionaries with:
   - id: Email ID
   - subject: Email subject
   - sender: Sender email
   - date: Email date
   - is_read: True/False
   - body: Email body (first 200 chars)
""")
