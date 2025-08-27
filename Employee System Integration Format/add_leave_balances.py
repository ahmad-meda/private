#!/usr/bin/env python3
"""
Simple function to add 10 leave balance records for an employee.
"""

from datetime import datetime, timezone
from Files.SQLAlchemyModels import LeaveBalance, Employee
from app import app, db

def add_leave_balances_for_employee(employee_id: int):
    """
    Add 10 leave balance records for the specified employee ID.
    
    Args:
        employee_id (int): The ID of the employee to add leave balances for
        
    Returns:
        dict: Result with success status and message
    """
    
    # Define the 10 leave types
    leave_types = [
        "Sick Leave",
        "Casual Leave", 
        "Annual / Privileged Leave",
        "Bereavement Leave",
        "Paternity Leave",
        "Maternity Leave",
        "Comp-Off",
        "WFH",
        "REMOTE",
        "TRAVEL"
    ]
    
    try:
        with app.app_context():
            # Check if employee exists
            employee = db.session.query(Employee).get(employee_id)
            if not employee:
                return {
                    'success': False,
                    'message': f"Employee with ID {employee_id} not found"
                }
            
            # Check if leave balances already exist
            existing_balances = db.session.query(LeaveBalance).filter(
                LeaveBalance.employee_id == employee_id
            ).all()
            
            if existing_balances:
                return {
                    'success': False,
                    'message': f"Leave balances already exist for employee {employee_id}"
                }
            
            # Create leave balance records
            leave_balance_records = []
            for leave_type in leave_types:
                leave_balance = LeaveBalance(
                    employee_id=employee_id,
                    request_type=leave_type,
                    balance=0.0,  # Start with 0 balance
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc)
                )
                leave_balance_records.append(leave_balance)
            
            # Add all records to database
            db.session.add_all(leave_balance_records)
            db.session.commit()
            
            return {
                'success': True,
                'message': f"Successfully created {len(leave_types)} leave balance records for employee {employee_id}",
                'leave_types': leave_types
            }
            
    except Exception as e:
        db.session.rollback()
        return {
            'success': False,
            'message': f"Error creating leave balances: {str(e)}"
        }

# Test function
def test_add_leave_balances():
    """Test the function with the first employee in the database"""
    
    with app.app_context():
        # Get first employee
        employee = db.session.query(Employee).first()
        if not employee:
            print("No employees found in database!")
            return
        
        print(f"Testing with employee: {employee.name} (ID: {employee.id})")
        
        # Call the function
        result = add_leave_balances_for_employee(employee.id)
        
        print(f"Result: {result}")
        
        if result['success']:
            print("✅ Success!")
            # Verify the records were created
            balances = db.session.query(LeaveBalance).filter(
                LeaveBalance.employee_id == employee.id
            ).all()
            
            print(f"Created {len(balances)} leave balance records:")
            for balance in balances:
                print(f"  - {balance.request_type}: {balance.balance} days")
        else:
            print("❌ Failed!")
            print(f"Error: {result['message']}")

if __name__ == "__main__":
    test_add_leave_balances()
