from Utils.agents import soft_delete_employee_extraction, soft_delete_employee_response
from Utils.choices import EmployeeChoices
from Utils.fuzzy_logic import find_best_match
from Utils.formats import SoftDeleteExtraction  
from proxies.employee_session_proxy import EmployeeSessionProxy
from proxies.proxy import EmployeeProxy
from Utils.fields_to_delete import agent_states
from proxies.employee_message_proxy import LeadMessageHistoryProxy
from Utils.sanitization import sanitize_messages
from Files.SQLAlchemyModels import Employee, Company, Group
from app import app, db

def find_deletable_employees(contact_number):
    """Find employees that can be deleted based on user's group and company permissions"""
    
    print("Finding deletable employees...")
    
    # Get the user's employee record to determine permissions
    try:
        employee_record = EmployeeProxy.get_employee_record(contact_number=contact_number)
        print(f"User: {employee_record.name}")
        print(f"Group ID: {employee_record.group_id}")
        print(f"Company ID: {employee_record.company_id}")
        
        # Query for employees based on permissions
        with app.app_context():
            query = db.session.query(Employee).filter(
                Employee.is_deleted == False  # Only non-deleted employees
            )
            
            if employee_record.group_id:
                # If user has a group, filter by group
                query = query.filter(Employee.group_id == employee_record.group_id)
                print(f"Filtering by group ID: {employee_record.group_id}")
            else:
                # If no group, filter by company
                query = query.filter(Employee.company_id == employee_record.company_id)
                print(f"Filtering by company ID: {employee_record.company_id}")
            
            # Get up to 10 employees
            employees = query.limit(10).all()
            
            if not employees:
                print("No employees found to delete.")
                return []
            
            print(f"\nFound {len(employees)} employees you can delete:")
            print("-" * 80)
            
            for i, emp in enumerate(employees, 1):
                # Skip the user themselves
                if emp.id == employee_record.id:
                    continue
                    
                print(f"{i}. ID: {emp.id}")
                print(f"   Name: {emp.name or 'N/A'}")
                print(f"   Employee ID: {emp.employeeId or 'N/A'}")
                print(f"   Contact: {emp.contactNo or 'N/A'}")
                print(f"   Email: {emp.emailId or 'N/A'}")
                print(f"   Designation: {emp.designation or 'N/A'}")
                print(f"   Company ID: {emp.company_id or 'N/A'}")
                print(f"   Group ID: {emp.group_id or 'N/A'}")
                print(f"   Department ID: {emp.department_id or 'N/A'}")
                print(f"   Role ID: {emp.role_id or 'N/A'}")
                print("-" * 80)
            
            return employees
            
    except Exception as e:
        print(f"Error finding deletable employees: {str(e)}")
        return []

def main():
    # Replace with your actual contact number
    contact_number = "+971501234567"
    
    deletable_employees = find_deletable_employees(contact_number)
    
    if deletable_employees:
        print(f"\nTotal employees you can delete: {len(deletable_employees)}")
        print("\nTo delete an employee, use the delete_employee.py script with their ID or name.")
    else:
        print("No employees found to delete.")

if __name__ == "__main__":
    main()
