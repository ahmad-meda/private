import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_huse_users():
    """Get users from Huse API"""
    base_url = os.environ.get('API_BASE_URL')
    token = os.environ.get('API_AUTH_TOKEN')
    
    headers = {"Authorization": token}
    url = f"{base_url}/api/Users"
    
    # Add parameters like in your curl command
    params = {
        'PageSize': 200
        
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        users = response.json()
        
        # Extract usernames
        usernames = [user['username'] for user in users]
        print(usernames)
        
        return usernames
    else:
        print(f"Error: {response.status_code}")
        return None


