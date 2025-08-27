#!/usr/bin/env python3
"""
Test script for Huse registration with draft employee data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from database import db
from Files.SQLAlchemyModels import EmployeeDraft
from huse.backend import register_employee_in_huse
from sqlalchemy.orm import Session


def test_huse_registration():
    """Test Huse registration with a draft employee record"""
    
    # Use Flask app context
    with app.app_context():
        # Create database session
        session = Session(db.engine)
    
    try:
        # Get the first available draft employee record
        draft_employee = session.query(EmployeeDraft).first()
        
        if not draft_employee:
            print("No draft employee records found in the database.")
            return
        
        print(f"Testing with draft employee: {draft_employee.name} (ID: {draft_employee.id})")
        print(f"Email: {draft_employee.email_id}")
        print(f"Contact: {draft_employee.contact_no}")
        print(f"Gender: {draft_employee.gender}")
        print("-" * 50)
        
        # Convert SQLAlchemy object to dictionary
        employee_data = {
            'id': draft_employee.id,
            'name': draft_employee.name,
            'emailId': draft_employee.email_id,
            'contactNo': draft_employee.contact_no,
            'gender': draft_employee.gender,
            'designation': draft_employee.designation,
            'dateOfJoining': draft_employee.date_of_joining,
            'dateOfBirth': draft_employee.date_of_birth,
            'first_name': draft_employee.first_name,
            'middle_name': draft_employee.middle_name,
            'last_name': draft_employee.last_name
        }
        
        print("Employee data prepared:")
        for key, value in employee_data.items():
            print(f"  {key}: {value}")
        print("-" * 50)
        
        # Test Huse registration
        print("Testing Huse registration...")
        result = register_employee_in_huse(employee_data)
        
        print("Registration result:")
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        
        if result.get('success'):
            credentials = result.get('credentials', {})
            print(f"Username: {credentials.get('username')}")
            print(f"Password: {credentials.get('password')}")
        
        if result.get('error'):
            print(f"Error: {result.get('error')}")
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        session.close()


if __name__ == "__main__":
    test_huse_registration()
