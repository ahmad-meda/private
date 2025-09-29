#!/usr/bin/env python3
"""
SUPER SIMPLE EMAIL READER - For Beginners
This code reads the last 5 emails from your inbox.
"""

# Step 1: Import the tools we need
import imaplib
import email
import os
from dotenv import load_dotenv

# Step 2: Load your email settings from .env file
load_dotenv()

def read_my_emails():
    """
    This function reads emails from your inbox.
    """
    
    # Step 3: Get your email and password from .env file
    my_email = os.environ.get('EMAIL_SENDER_ADDRESS')
    my_password = os.environ.get('EMAIL_SENDER_PASSWORD')
    
    # Step 4: Check if we have email settings
    if not my_email or not my_password:
        print("❌ ERROR: Please set your email in .env file")
        print("Add these lines to your .env file:")
        print("EMAIL_SENDER_ADDRESS=your-email@gmail.com")
        print("EMAIL_SENDER_PASSWORD=your-password")
        return
    
    try:
        # Step 5: Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(my_email, my_password)
        
        # Step 6: Open inbox
        mail.select("inbox")
        
        # Step 7: Get all email IDs
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()
        
        # Step 8: Get the last 5 emails
        last_5_emails = email_ids[-5:] if len(email_ids) >= 5 else email_ids
        
        # Step 9: Read each email
        for i, email_id in enumerate(last_5_emails, 1):
            # Get the email
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            # Get email details
            subject = email_message["Subject"]
            sender = email_message["From"]
            date = email_message["Date"]
            
            # Show the email
            print(f"{i}. SUBJECT: {subject}")
            print(f"   FROM: {sender}")
            print(f"   DATE: {date}")
            print()
        
        # Step 10: Close connection
        mail.close()
        mail.logout()
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print("\n💡 TIPS:")
        print("1. Make sure you're using Gmail")
        print("2. Enable 2-factor authentication in Gmail")
        print("3. Generate an 'App Password' in Gmail")
        print("4. Use the App Password (not your regular password)")

# read_my_emails()