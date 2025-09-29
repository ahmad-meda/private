import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def get_huse_user_by_username(username):
    """Get complete Huse user record by username"""
    try:
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        if not base_url or not token:
            print("Error: API_BASE_URL and API_AUTH_TOKEN must be set")
            return None
        
        headers = {"Authorization": token}
        
        # First, get all users to find the user ID
        url = f"{base_url}/api/Users"
        params = {'PageSize': 10000000}
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            users = response.json()
            
            # Search for user by username to get the ID
            user_id = None
            for user in users:
                if isinstance(user, dict) and user.get('username'):
                    if user.get('username').strip().lower() == username.strip().lower():
                        user_id = user.get('id')
                        break
            
            if not user_id:
                print(f"No user found with username: {username}")
                return None
            
            # Now get the complete user record using the full endpoint
            full_url = f"{base_url}/api/Users/full/{user_id}"
            full_response = requests.get(full_url, headers=headers, timeout=30)
            
            if full_response.status_code == 200:
                print(f"Found complete user record for username: {username} (ID: {user_id})")
                return full_response.json()
            else:
                print(f"API Error getting full user record: {full_response.status_code}")
                return None
        else:
            print(f"API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error getting user record from API: {e}")
        return None
        
def update_user_record(username, contact_number: Optional[str] = None, email: Optional[str] = None):
    """Get user record by username, then only update the contact or email"""
    try:
        # First get the current user record
        user_record = get_huse_user_by_username(username)
        if not user_record:
            print(f"User not found: {username}")
            return None
        
        # ONLY update the specific fields requested - DO NOT touch any other fields
        # The user record from get_huse_user_by_username already contains all the data
        # We only modify the fields that were explicitly requested
        
        # Create a copy to avoid modifying the original record
        updated_record = user_record.copy()
        
        # Only update contact if provided
        if contact_number is not None:
            updated_record['contact'] = contact_number
            print(f"Updating contact number to: {contact_number}")
        
        # Only update email if provided  
        if email is not None:
            updated_record['email'] = email
            print(f"Updating email to: {email}")
        
        # IMPORTANT: All other fields remain EXACTLY the same as they were
        # The API requires the complete record with all original values preserved
        
        # Debug: Print what we're sending to the API
        print(f"Sending record to API with {len(updated_record)} fields")
        print(f"Contact field: {updated_record.get('contact')}")
        print(f"Email field: {updated_record.get('email')}")
        print(f"SecurityAnswer field: {updated_record.get('securityAnswer')}")
        
        # Make the API call to update the user
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        if not base_url or not token:
            print("Error: API_BASE_URL and API_AUTH_TOKEN must be set")
            return None
        
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        url = f"{base_url}/api/Users"
        
        response = requests.put(url, headers=headers, json=updated_record, timeout=30)
        
        if response.status_code == 200:
            print(f"Successfully updated user record for: {username}")
            return response.json()
        else:
            print(f"API Error updating user: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error updating user record: {e}")
        return None
