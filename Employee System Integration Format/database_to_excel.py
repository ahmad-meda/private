#!/usr/bin/env python3
"""
Database to Excel Export Script
This script reads data from the Employee database and exports it to Excel,
then lists all usernames from the username column.
"""

import os
import sys
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add the current directory to Python path to import our models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Files.SQLAlchemyModels import Employee, Company, Department, Role, Group, OfficeLocation
from database import db

# Load environment variables
load_dotenv()

def get_database_connection():
    """Get database connection using the same configuration as the app"""
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:ias12345@localhost:5432/Employee")
    engine = create_engine(database_url)
    return engine

def export_employees_to_excel():
    """Export all employee data to Excel and list usernames"""
    
    print("🔄 Connecting to database...")
    engine = get_database_connection()
    
    try:
        # Query to get all employee data with related information
        query = """
        SELECT 
            e.id,
            e."employeeId",
            e.first_name,
            e.middle_name,
            e.last_name,
            e.name,
            e."emailId",
            e.designation,
            e."dateOfJoining",
            e."dateOfBirth",
            e."contactNo",
            e.gender,
            e.username,
            e.password,
            e.is_hr,
            e.hr_scope,
            e.allow_site_checkin,
            e.restrict_to_allowed_locations,
            e.reminders,
            e.is_deleted,
            e.deleted_at,
            e.created_by,
            c.name as company_name,
            d.name as department_name,
            r.name as role_name,
            g.name as group_name,
            ol.name as office_location_name,
            ol.address as office_address,
            ol.latitude as office_latitude,
            ol.longitude as office_longitude
        FROM employee e
        LEFT JOIN companies c ON e.company_id = c.id
        LEFT JOIN department d ON e.department_id = d.id
        LEFT JOIN role r ON e.role_id = r.id
        LEFT JOIN groups g ON e.group_id = g.id
        LEFT JOIN office_locations ol ON e.office_location_id = ol.id
        WHERE e.is_deleted = false OR e.is_deleted IS NULL
        ORDER BY e.id;
        """
        
        print("📊 Fetching employee data from database...")
        df = pd.read_sql_query(query, engine)
        
        if df.empty:
            print("❌ No employee data found in the database.")
            return
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = f"employee_data_export_{timestamp}.xlsx"
        
        print(f"📝 Exporting data to Excel file: {excel_filename}")
        
        # Export to Excel with formatting
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            # Main employee data sheet
            df.to_excel(writer, sheet_name='Employee Data', index=False)
            
            # Get the workbook and worksheet for formatting
            workbook = writer.book
            worksheet = writer.sheets['Employee Data']
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"✅ Successfully exported {len(df)} employee records to {excel_filename}")
        
        # List all usernames
        print("\n" + "="*60)
        print("👥 USERNAMES FOUND IN DATABASE:")
        print("="*60)
        
        # Filter out null/empty usernames
        usernames = df['username'].dropna()
        usernames = usernames[usernames != '']
        
        if usernames.empty:
            print("❌ No usernames found in the database.")
        else:
            print(f"📋 Total usernames found: {len(usernames)}")
            print("\nList of usernames:")
            print("-" * 40)
            
            for i, username in enumerate(usernames.unique(), 1):
                print(f"{i:3d}. {username}")
            
            # Also save usernames to a separate sheet
            username_df = pd.DataFrame({
                'Username': usernames.unique(),
                'Count': [len(df[df['username'] == username]) for username in usernames.unique()]
            })
            username_df = username_df.sort_values('Username')
            
            with pd.ExcelWriter(excel_filename, engine='openpyxl', mode='a') as writer:
                username_df.to_excel(writer, sheet_name='Usernames', index=False)
            
            print(f"\n💾 Usernames also saved to 'Usernames' sheet in {excel_filename}")
        
        # Display summary statistics
        print("\n" + "="*60)
        print("📈 SUMMARY STATISTICS:")
        print("="*60)
        print(f"Total employees: {len(df)}")
        print(f"Employees with usernames: {len(usernames)}")
        print(f"Employees without usernames: {len(df) - len(usernames)}")
        print(f"Companies: {df['company_name'].nunique()}")
        print(f"Departments: {df['department_name'].nunique()}")
        print(f"Roles: {df['role_name'].nunique()}")
        print(f"Office locations: {df['office_location_name'].nunique()}")
        
        return excel_filename
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        return None
    finally:
        engine.dispose()

def main():
    """Main function to run the export process"""
    print("🚀 Starting Database to Excel Export Process")
    print("="*60)
    
    # Check if required packages are available
    try:
        import pandas as pd
        import openpyxl
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install required packages: pip install pandas openpyxl")
        return
    
    # Run the export
    excel_file = export_employees_to_excel()
    
    if excel_file:
        print(f"\n🎉 Process completed successfully!")
        print(f"📁 Excel file created: {excel_file}")
        print(f"📍 File location: {os.path.abspath(excel_file)}")
    else:
        print("\n❌ Process failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
