import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_huse_users():
    """Get all users from Huse API"""
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
            return users
        else:
            print(f"API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error getting Huse users: {e}")
        return None

def update_user_status(user_id, status, remarks=None):
    """Update user status in Huse"""
    try:
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        headers = {"Authorization": token}
        
        # Prepare form data for the API request (using correct field names)
        form_data = {
            "UserId": str(user_id),
            "AccountStatus": str(status)
        }
        
        if remarks:
            form_data["Remarks"] = remarks
        
        # Use PUT method and correct endpoint
        url = f"{base_url}/api/Users/update_status"
        response = requests.put(url, headers=headers, data=form_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json() if response.text else {}
            return {'success': True, 'data': result}
        else:
            error_msg = f"HTTP {response.status_code}"
            try:
                error_detail = response.json()
                error_msg = error_detail.get('message', error_msg)
            except:
                error_msg = response.text or error_msg
            return {'success': False, 'message': error_msg}
            
    except Exception as e:
        return {'success': False, 'message': str(e)}

def update_status_for_all_users():
    """Update status to 3 for ALL users in Huse"""
    
    print("Getting all users from Huse...")
    
    # Get all users from Huse
    users = get_huse_users()
    if not users:
        print("Failed to get users from Huse")
        return
    
    print(f"Found {len(users)} users in Huse")
    print("Updating status to 3 for all users...")
    
    # Update status for each user
    updated_count = 0
    already_status_3_count = 0
    failed_count = 0
    
    for user in users:
        if not isinstance(user, dict):
            print(f"⚠️ Skipping invalid user data: {user}")
            continue
            
        user_id = user.get('id')
        username = user.get('username', 'Unknown')
        user_name = user.get('name', 'Unknown')
        current_status = user.get('status')
        
        if not user_id:
            print(f"⚠️ Skipping user {username} - no user ID")
            continue
        
        # Check if status is already 3
        if current_status == 3:
            print(f"✅ {username} ({user_name}) - Status already 3, skipping")
            already_status_3_count += 1
            continue
        
        print(f"Updating status for {username} (ID: {user_id}, Name: {user_name}) from {current_status} to 3...")
        result = update_user_status(user_id, 3, "Status updated to 3")
        
        if result['success']:
            print(f"✅ Successfully updated status for {username}")
            updated_count += 1
        else:
            print(f"❌ Failed to update status for {username}: {result['message']}")
            failed_count += 1
    
    print(f"\n📊 Summary:")
    print(f"✅ Successfully updated: {updated_count}")
    print(f"✅ Already status 3: {already_status_3_count}")
    print(f"❌ Failed updates: {failed_count}")
    print(f"📝 Total users processed: {len(users)}")

if __name__ == "__main__":
    update_status_for_all_users()
