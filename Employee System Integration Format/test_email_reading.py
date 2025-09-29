#!/usr/bin/env python3
"""
Test email reading with your current setup.
"""

import imaplib
import email
from email.header import decode_header
import os
from email_config import EMAIL_SENDER_ADDRESS, EMAIL_SENDER_PASSWORD, IMAP_HOST, IMAP_PORT

def test_read_emails():
    """
    Test reading emails using your current email setup.
    """
    email_address = EMAIL_SENDER_ADDRESS
    email_password = EMAIL_SENDER_PASSWORD
    
    if not email_address or not email_password:
        print("❌ Please configure your email in email_config.py")
        print("1. Open email_config.py")
        print("2. Set your Huse email address and password")
        return
    
    print(f"📧 Testing email reading for: {email_address}")
    print("=" * 60)
    
    try:
        # Connect to Huse email IMAP
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
        mail.login(email_address, email_password)
        
        # Select inbox
        mail.select("inbox")
        
        # Search for emails
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()
        
        print(f"📊 Total emails in inbox: {len(email_ids)}")
        
        # Get last 5 emails
        latest_emails = email_ids[-5:] if len(email_ids) >= 5 else email_ids
        
        print(f"📋 Reading last {len(latest_emails)} emails:")
        print("-" * 60)
        
        for i, email_id in enumerate(latest_emails, 1):
            # Fetch email
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            # Extract subject
            subject = decode_header(email_message["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            
            # Extract sender
            sender = decode_header(email_message["From"])[0][0]
            if isinstance(sender, bytes):
                sender = sender.decode()
            
            # Extract date
            date = email_message["Date"]
            
            print(f"{i}. Subject: {subject}")
            print(f"   From: {sender}")
            print(f"   Date: {date}")
            print()
        
        mail.close()
        mail.logout()
        
        print("✅ Email reading test completed successfully!")
        
    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP Error: {str(e)}")
        print("💡 This might be because:")
        print("   - Huse email credentials are incorrect")
        print("   - IMAP is not enabled on your Huse email account")
        print("   - IMAP server settings are wrong")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_read_emails()
