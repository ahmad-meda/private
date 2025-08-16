from app import app, db
from Files.SQLAlchemyModels import Employee
from datetime import datetime

with app.app_context():
    # Create a new James Rogan with different details
    new_james_rogan = Employee(
        name="James Rogan",
        contactNo="+971501234568",  # Different contact number
        emailId="james.rogan2@company.com",  # Different email
        employeeId="EMP002",  # Different employee ID
        designation="Senior Developer",  # Different designation
        dateOfJoining=datetime(2023, 6, 15),  # Different joining date
        dateOfBirth=datetime(1985, 8, 20),  # Different birth date
        gender="Male",
        group_id=3,  # Same group as current HR user
        company_id=3,  # Same company as current HR user
        is_deleted=False
    )
    
    try:
        db.session.add(new_james_rogan)
        db.session.commit()
        print(f"Successfully added new James Rogan with ID: {new_james_rogan.id}")
        print(f"Contact: {new_james_rogan.contactNo}")
        print(f"Email: {new_james_rogan.emailId}")
        print(f"Employee ID: {new_james_rogan.employeeId}")
        print(f"Designation: {new_james_rogan.designation}")
    except Exception as e:
        print(f"Error adding employee: {e}")
        db.session.rollback() 