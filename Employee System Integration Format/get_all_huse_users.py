#!/usr/bin/env python3
"""
Script to get all users from Huse app with their details:
- Contact number
- Name
- Username
- Gender
- Email
"""

import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_all_huse_users():
    """Get all users from Huse API with detailed information"""
    try:
        # Get environment variables
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        if not base_url or not token:
            print("❌ Error: API_BASE_URL and API_AUTH_TOKEN must be set in .env file")
            return None
        
        # Validate URL format
        if not base_url.startswith(('http://', 'https://')):
            print("❌ Error: API_BASE_URL must start with http:// or https://")
            return None
        
        print(f"🔗 Connecting to Huse API: {base_url}")
        
        headers = {"Authorization": token}
        url = f"{base_url}/api/Users"
        
        # Request all users with a large page size
        params = {'PageSize': 10000}  # Large number to get all users
        
        print("📡 Fetching users from Huse API...")
        response = requests.get(url, headers=headers, params=params, timeout=60)
        
        if response.status_code == 200:
            try:
                users = response.json()
                
                # Validate response format
                if not isinstance(users, list):
                    print("❌ Error: API response is not a list")
                    return None
                
                print(f"✅ Successfully retrieved {len(users)} users from Huse")
                return users
                
            except ValueError as e:
                print(f"❌ Error: Invalid JSON response from API - {e}")
                return None
                
        else:
            print(f"❌ API Error: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Error details: {error_detail}")
            except:
                print(f"Error response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Error: API request timed out after 60 seconds")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to Huse API. Check your internet connection and API_BASE_URL")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def format_user_data(users):
    """Format user data for display and export"""
    if not users:
        return []
    
    formatted_users = []
    
    for i, user in enumerate(users):
        if not isinstance(user, dict):
            print(f"⚠️ Warning: User at index {i} is not a dictionary, skipping")
            continue
        
        # Extract user information with safe defaults
        user_data = {
            'ID': user.get('id', 'N/A'),
            'Name': user.get('name', 'N/A'),
            'Username': user.get('username', 'N/A'),
            'Email': user.get('email', 'N/A'),
            'Contact': user.get('contact', 'N/A'),
            'Gender': user.get('gender', 'N/A'),
            'Status': user.get('status', 'N/A'),
            'Created_At': user.get('createdAt', 'N/A'),
            'Updated_At': user.get('updatedAt', 'N/A')
        }
        
        formatted_users.append(user_data)
    
    return formatted_users

def display_users_table(users_data):
    """Display users in a formatted table"""
    if not users_data:
        print("❌ No user data to display")
        return
    
    print("\n" + "="*120)
    print("📋 ALL HUSE USERS")
    print("="*120)
    
    # Create DataFrame for better formatting
    df = pd.DataFrame(users_data)
    
    # Display basic info
    print(f"📊 Total Users: {len(users_data)}")
    print(f"📅 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n")
    
    # Display table with selected columns
    display_columns = ['ID', 'Name', 'Username', 'Email', 'Contact', 'Gender', 'Status']
    print(df[display_columns].to_string(index=False, max_colwidth=30))
    
    print("\n" + "="*120)

def export_to_excel(users_data, filename=None):
    """Export user data to Excel file"""
    if not users_data:
        print("❌ No user data to export")
        return False
    
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"huse_users_{timestamp}.xlsx"
    
    try:
        df = pd.DataFrame(users_data)
        df.to_excel(filename, index=False, sheet_name='Huse Users')
        print(f"✅ User data exported to: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error exporting to Excel: {e}")
        return False

def export_to_csv(users_data, filename=None):
    """Export user data to CSV file"""
    if not users_data:
        print("❌ No user data to export")
        return False
    
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"huse_users_{timestamp}.csv"
    
    try:
        df = pd.DataFrame(users_data)
        df.to_csv(filename, index=False)
        print(f"✅ User data exported to: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error exporting to CSV: {e}")
        return False

def main():
    """Main function to run the script"""
    print("🚀 Starting Huse Users Export Script")
    print("="*50)
    
    # Get all users from Huse
    users = get_all_huse_users()
    
    if not users:
        print("❌ Failed to retrieve users from Huse API")
        return
    
    # Format user data
    formatted_users = format_user_data(users)
    
    if not formatted_users:
        print("❌ No valid user data found")
        return
    
    # Display users in table format
    display_users_table(formatted_users)
    
    # Export to Excel
    excel_success = export_to_excel(formatted_users)
    
    # Export to CSV
    csv_success = export_to_csv(formatted_users)
    
    # Summary
    print("\n" + "="*50)
    print("📋 SUMMARY")
    print("="*50)
    print(f"✅ Total users retrieved: {len(formatted_users)}")
    print(f"📊 Excel export: {'✅ Success' if excel_success else '❌ Failed'}")
    print(f"📊 CSV export: {'✅ Success' if csv_success else '❌ Failed'}")
    print("="*50)

if __name__ == "__main__":
    main()
