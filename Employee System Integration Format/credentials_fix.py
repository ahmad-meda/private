import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_huse_users_with_ids():
    """Get users from Huse API with both usernames and IDs"""
    try:
        # Validate environment variables
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        if not base_url or not token:
            print("Error: API_BASE_URL and API_AUTH_TOKEN must be set")
            return None
        
        # Validate URL format
        if not base_url.startswith(('http://', 'https://')):
            print("Error: API_BASE_URL must start with http:// or https://")
            return None
        
        headers = {"Authorization": f"Bearer {token}"}
        url = f"{base_url}/api/Users"
        
        # Add parameters like in your curl command
        params = {
            'PageSize': 1000
        }
        
        # Make request with timeout
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            try:
                users = response.json()
                
                # Validate response format
                if not isinstance(users, list):
                    print("Error: API response is not a list")
                    return None
                
                # Create a dictionary mapping usernames to IDs
                username_to_id = {}
                for i, user in enumerate(users):
                    if not isinstance(user, dict):
                        print(f"Warning: User at index {i} is not a dictionary, skipping")
                        continue
                    
                    if 'username' not in user or 'id' not in user:
                        print(f"Warning: User at index {i} missing 'username' or 'id' field, skipping")
                        continue
                    
                    username = user['username']
                    user_id = user['id']
                    
                    if username and isinstance(username, str) and username.strip():
                        username_to_id[username.strip()] = user_id
                
                print(f"Successfully retrieved {len(username_to_id)} users from Huse")
                return username_to_id
                
            except ValueError as e:
                print(f"Error: Invalid JSON response from API - {e}")
                return None
                
        else:
            print(f"API Error: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Error details: {error_detail}")
            except:
                print(f"Error response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("Error: API request timed out after 30 seconds")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed - {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in get_huse_users_with_ids: {e}")
        return None

def delete_huse_user(user_id):
    """Delete a user from Huse using their ID"""
    try:
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        if not base_url or not token:
            print("Error: API_BASE_URL and API_AUTH_TOKEN must be set")
            return False
        
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        url = f"{base_url}/api/Users/permanent/{user_id}"
        
        response = requests.delete(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to delete user ID {user_id}: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Error details: {error_detail}")
            except:
                print(f"Error response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"Timeout deleting user ID {user_id}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Request error deleting user ID {user_id}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error deleting user ID {user_id}: {e}")
        return False

def get_usernames_from_excel(excel_file_path="employees.xlsx"):
    """Get usernames from Excel file"""
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file_path)
        
        # Check if 'App Username' column exists
        if 'App Username' not in df.columns:
            print(f"Error: 'App Username' column not found in {excel_file_path}")
            print(f"Available columns: {list(df.columns)}")
            return None
        
        # Get usernames, removing any NaN values
        usernames = df['App Username'].dropna().tolist()
        
        # Convert to strings and strip whitespace
        usernames = [str(username).strip() for username in usernames if str(username).strip()]
        
        print(f"Successfully loaded {len(usernames)} usernames from {excel_file_path}")
        return usernames
        
    except FileNotFoundError:
        print(f"Error: Excel file '{excel_file_path}' not found")
        return None
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def delete_all_huse_users():
    """Delete all users from Huse that exist in our Excel file"""
    # Get usernames from Excel file
    usernames = get_usernames_from_excel()
    
    if not usernames:
        print("Could not retrieve usernames from Excel file. Cannot proceed with deletion.")
        return
    
    # Get Huse users with IDs
    huse_users = get_huse_users_with_ids()
    
    if not huse_users:
        print("Could not retrieve Huse users. Cannot proceed with deletion.")
        return
    
    print(f"\nFound {len(usernames)} usernames in Excel file:")
    print("-" * 50)
    
    # Collect all IDs to delete
    ids_to_delete = []
    for i, username in enumerate(usernames, 1):
        huse_id = huse_users.get(username, None)
        if huse_id:
            ids_to_delete.append(huse_id)
            print(f"{i:3d}. {username:<20} | ID: {huse_id}")
        else:
            print(f"{i:3d}. {username:<20} | ID: Not found in Huse")
    
    if not ids_to_delete:
        print("\nNo users found in Huse to delete.")
        return
    
    print(f"\n{'='*60}")
    print(f"WARNING: About to PERMANENTLY DELETE {len(ids_to_delete)} users from Huse!")
    print(f"{'='*60}")
    print("Proceeding with deletion automatically...")
    
    print(f"\nStarting deletion of {len(ids_to_delete)} users...")
    print("-" * 50)
    
    successful_deletions = 0
    failed_deletions = 0
    
    for i, user_id in enumerate(ids_to_delete, 1):
        print(f"Deleting user ID {user_id} ({i}/{len(ids_to_delete)})...", end=" ")
        
        if delete_huse_user(user_id):
            print("✓ Success")
            successful_deletions += 1
        else:
            print("✗ Failed")
            failed_deletions += 1
    
    print(f"\n{'='*60}")
    print(f"DELETION SUMMARY:")
    print(f"Successful deletions: {successful_deletions}")
    print(f"Failed deletions: {failed_deletions}")
    print(f"Total processed: {len(ids_to_delete)}")
    print(f"{'='*60}")

# Run the deletion process
delete_all_huse_users()