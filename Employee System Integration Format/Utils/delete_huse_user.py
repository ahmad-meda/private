import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_user_id_by_username(username):
    """Get user ID from Huse API by username"""
    try:
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        if not base_url or not token:
            print("Error: API_BASE_URL and API_AUTH_TOKEN must be set")
            return None
        
        headers = {"Authorization": token}
        url = f"{base_url}/api/Users"
        params = {'PageSize': 1000}
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            users = response.json()
            
            for user in users:
                if isinstance(user, dict) and user.get('username') == username:
                    return user.get('id')
            
            return "User isn't registered in Huse"
        else:
            print(f"API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def delete_user_by_username(username):
    """Delete user from Huse by username"""
    try:
        # Get user ID by username
        user_id = get_user_id_by_username(username)
        
        if not user_id:
            print(f"❌ {user_id}")
            return False
        
        # Delete user by ID
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        headers = {
            "accept": "application/json",
            "Authorization": token
        }
        
        url = f"{base_url}/api/Users/{user_id}"
        
        response = requests.delete(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ User '{username}' (ID: {user_id}) deleted successfully!")
            return True
        else:
            print(f"❌ Failed to delete user '{username}': {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error deleting user '{username}': {e}")
        return False