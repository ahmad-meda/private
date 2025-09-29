import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_huse_users_details():
    """Get all users from Huse API"""
    try:
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        headers = {"Authorization": token}
        url = f"{base_url}/api/Users"
        params = {'PageSize': 1000}
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            users = response.json()
            print(f"Found {len(users)} users in Huse")
            return users
        else:
            print(f"API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def find_user_id_by_mobile(mobile):
    """Find user ID matching mobile number"""
    users = get_huse_users_details()
    if not users:
        return None
    
    mobile = mobile.lower().strip()
    
    for user in users:
        if not isinstance(user, dict):
            continue
        
        user_id = user.get('id')
        user_mobile = user.get('contact', user.get('phone', '')).lower().strip()
        
        # Check if mobile matches
        if mobile in user_mobile:
            return user_id
    
    return None

def find_user_id_by_email(email):
    """Find user ID matching email"""
    users = get_huse_users_details()
    if not users:
        return None
    
    email = email.lower().strip()
    
    for user in users:
        if not isinstance(user, dict):
            continue
        
        user_id = user.get('id')
        user_email = user.get('email', '').lower().strip()
        
        # Check if email matches
        if email in user_email:
            return user_id
    
    return None

def delete_user_by_id(user_id):
    """Delete a user from Huse using their ID"""
    try:
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        headers = {
            "accept": "application/json",
            "Authorization": token
        }
        
        url = f"{base_url}/api/Users/permanent/{user_id}"
        
        response = requests.delete(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ User ID {user_id} deleted successfully!")
            return True
        else:
            print(f"❌ Failed to delete user ID {user_id}: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Error details: {error_detail}")
            except:
                print(f"Error response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ Timeout deleting user ID {user_id}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error deleting user ID {user_id}: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error deleting user ID {user_id}: {e}")
        return False

# Example usage:
# Mobile search
mobile_id = find_user_id_by_mobile("+971509565289")
print(f"Mobile search result: {mobile_id}")

# Email search  
email_id = find_user_id_by_email("yobozyt@gmail.com")
print(f"Email search result: {email_id}")

# Delete user by ID
if mobile_id:
    delete_user_by_id(mobile_id)