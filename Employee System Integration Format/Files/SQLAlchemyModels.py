from sqlalchemy import Double, Float, create_engine, Column, Integer, String, DateTime, Boolean, Text, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

from database import db

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:ias12345@localhost:5432/Employee")

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Association table for many-to-many relationship between Employee and OfficeLocation
allowed_office_locations = db.Table(
    'allowed_office_locations',
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True),
    db.Column('office_location_id', db.Integer, db.ForeignKey('office_locations.id'), primary_key=True)
)

draft_allowed_office_locations = db.Table(
    'draft_allowed_office_locations',
    db.Column('draft_employee_id', db.Integer, db.ForeignKey('draft_employee.id'), primary_key=True),
    db.Column('office_location_id', db.Integer, db.ForeignKey('office_locations.id'), primary_key=True)
)

class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employeeId = db.Column(db.String(50), nullable=True)

    # 🔤 Name breakdown (new fields)
    first_name = db.Column(db.String(50), nullable=True)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)

    # 🧾 Keep full name for legacy code support
    name = db.Column(db.String, nullable=True)

    emailId = db.Column(db.String(100), nullable=True)
    designation = db.Column(db.String, nullable=True)
    dateOfJoining = db.Column(Date, nullable=True)

    dateOfBirth = db.Column(db.Date, nullable=True)
    contactNo = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=True)

    # 🔗 Office Location (instead of latitude/longitude directly)
    office_location_id = db.Column(db.Integer, ForeignKey('office_locations.id'), nullable=True)
    office_location = relationship('OfficeLocation', backref='employee')

    allowed_office_locations = relationship(
        'OfficeLocation',
        secondary=allowed_office_locations,
        backref='employees'
    )
    

    work_policy_id = db.Column(db.Integer, ForeignKey('work_policies.id'), nullable=True)
    work_policy = relationship('WorkPolicy', backref='employee')

    # Optional home location if policy requires it
    home_latitude = db.Column(db.Float, nullable=True)
    home_longitude = db.Column(db.Float, nullable=True)

    # 🔗 Company and Reporting Hierarchy
    company_id = db.Column(db.Integer, ForeignKey('companies.id'), nullable=True)
    company = relationship('Company', backref='employee')

    group_id = db.Column(db.Integer, ForeignKey('groups.id'), nullable=True)
    group = relationship('Group', backref='employee')

    reporting_manager_id = db.Column(db.Integer, ForeignKey('employee.id'), nullable=True)
    reporting_manager = relationship("Employee", remote_side=[id], backref="subordinates")

    # 🔗 Roles and Department
    role_id = db.Column(db.Integer, ForeignKey('role.id'), nullable=True)
    department_id = db.Column(db.Integer, ForeignKey('department.id'), nullable=True)

    role = relationship('Role', back_populates='employee')
    department = relationship('Department', back_populates='employee')
    reminders = db.Column(db.Boolean, nullable=False, default=True)
    allowed_company_ids = db.Column(db.JSON, nullable=True)
    is_hr = db.Column(db.Boolean, default=False, nullable=False)
    hr_scope = db.Column(db.String, default="company")
    allow_site_checkin = db.Column(db.Boolean, default=False)
    restrict_to_allowed_locations = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)

    # 🔗 Leave Requests and Balances
    leave_requests = relationship(
        "LeaveRequest",
        back_populates="employee",
        cascade="all, delete",
        foreign_keys="[LeaveRequest.employee_id]"
    )

    leave_balances = relationship(
        "LeaveBalance",
        back_populates="employee",
        cascade="all, delete",
        foreign_keys="[LeaveBalance.employee_id]"
    )
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    attendance = relationship("Attendance", back_populates="employee")
    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.name}')>"
    
class EmployeeDraft(db.Model):
    __tablename__ = "draft_employee"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(50), nullable=True)

    # 🔤 Name breakdown (new fields)
    first_name = db.Column(db.String(50), nullable=True)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)

    # 🧾 Keep full name for legacy code support
    name = db.Column(db.String, nullable=True)

    email_id = db.Column(db.String(100), nullable=True)
    designation = db.Column(db.String, nullable=True)
    date_of_joining = db.Column(Date, nullable=True)

    date_of_birth = db.Column(Date, nullable=True)
    contact_no = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=True)

    # 🔗 Office Location (instead of latitude/longitude directly)
    office_location_id = db.Column(db.Integer, ForeignKey('office_locations.id'), nullable=True)
    office_location = relationship('OfficeLocation', backref='draft_employee')

    allowed_office_locations = relationship(
        'OfficeLocation',
        secondary=draft_allowed_office_locations,
        backref='draft_employees'
    )

    work_policy_id = db.Column(db.Integer, ForeignKey('work_policies.id'), nullable=True)
    work_policy = relationship('WorkPolicy', backref='draft_employee')

    # Optional home location if policy requires it
    home_latitude = db.Column(db.Float, nullable=True)
    home_longitude = db.Column(db.Float, nullable=True)

    # 🔗 Company and Reporting Hierarchy
    company_id = db.Column(db.Integer, ForeignKey('companies.id'), nullable=True)
    company = relationship('Company', backref='draft_employee')

    group_id = db.Column(db.Integer, ForeignKey('groups.id'), nullable=True)
    group = relationship('Group', backref='draft_employee')

    reporting_manager_id = db.Column(db.Integer, ForeignKey('draft_employee.id'), nullable=True)
    reporting_manager = relationship("EmployeeDraft", remote_side=[id], backref="subordinates")

    # 🔗 Roles and Department
    role_id = db.Column(db.Integer, ForeignKey('role.id'), nullable=True)
    department_id = db.Column(db.Integer, ForeignKey('department.id'), nullable=True)

    role = relationship('Role', back_populates='draft_employee')
    department = relationship('Department', back_populates='draft_employee')

    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    reminders = db.Column(db.Boolean, nullable=False, default=True)
    allowed_company_ids = db.Column(db.JSON, nullable=True)
    is_hr = db.Column(db.Boolean, default=False, nullable=False)
    hr_scope = db.Column(db.String, default="company")
    allow_site_checkin = db.Column(db.Boolean, default=False)
    restrict_to_allowed_locations = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<EmployeeDraft(id={self.id}, name='{self.name}', department='{self.department.name if self.department else None}')>"

class Company(db.Model):
    __tablename__ = "companies"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prefix = db.Column(db.String(10))
    name = db.Column(db.String(255), nullable=False)
    group_id = db.Column(db.Integer, ForeignKey("groups.id"))
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"


class Group(db.Model):
    __tablename__ = "groups"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"


class Role(db.Model):
    __tablename__ = "role"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    # Add this relationship back to Employee
    employee = relationship('Employee', back_populates='role')
    draft_employee = relationship('EmployeeDraft', back_populates='role')
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"


class Department(db.Model):
    __tablename__ = "department"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    # Add this relationship back to Employee
    employee = relationship('Employee', back_populates='department')
    draft_employee = relationship('EmployeeDraft', back_populates='department')
    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}')>"


# class ReportingManager(Base):
#     __tablename__ = "reporting_managers"
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     manager_name = Column(String(255), nullable=False)
    
#     def __repr__(self):
#         return f"<ReportingManager(id={self.id}, manager_name='{self.manager_name}')>"


class OfficeLocation(db.Model):
    __tablename__ = "office_locations"
    
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # name = db.Column(db.String(255), nullable=False)
    id = db.Column(db.Integer, primary_key=True)    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)    
    name = db.Column(db.String(100), nullable=False)    
    address = db.Column(db.Text, nullable=True)    
    latitude = db.Column(db.Float, nullable=True)    
    longitude = db.Column(db.Float, nullable=True)    
    radius_meters = db.Column(db.Float, default=500)    
    is_active = db.Column(db.Boolean, default=True)    
    created_at = db.Column(db.DateTime, default=db.func.now())    
    company = db.relationship("Company", backref=db.backref("office_locations", lazy=True))    
    
    def __repr__(self):        return f"<OfficeLocation {self.name} - Company {self.company_id}>"
    
class WorkPolicy(db.Model):
    __tablename__ = "work_policies"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<WorkPolicy(id={self.id}, name='{self.name}')>"
    
class Draft(db.Model):
    __tablename__ = "drafts"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    draft_id = db.Column(db.String(100))
    draft_type = db.Column(db.String(100))
    employee_id = db.Column(db.Integer)
    
    def __repr__(self):
        return f"<Draft(id={self.id}, draft_id='{self.draft_id}', draft_type='{self.draft_type}')>"
    
class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, ForeignKey('employee.id'), nullable=False)
    
    # Relationship back to Employee
    employee = relationship('Employee', back_populates='leave_requests')
    def __repr__(self):
        return f"<LeaveRequest(id={self.id}, employee_id={self.employee_id})>"


class LeaveBalance(db.Model):
    __tablename__ = 'leave_balances'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, ForeignKey('employee.id'), nullable=False)

    # Relationship back to Employee
    employee = relationship('Employee', back_populates='leave_balances')


    def __repr__(self):
        return f"<LeaveBalance(id={self.id}, employee_id={self.employee_id})>"

class LeadMessageHistory(db.Model):
    __tablename__ = "messages"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_number = db.Column(db.String)
    role = db.Column(db.String)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<LeadMessageHistory(id={self.id}, contact_number='{self.contact_number}', role='{self.role}', timestamp='{self.timestamp}')>"
    
class Attendance(db.Model):
    __tablename__ = 'attendance'  

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, ForeignKey('employee.id'), nullable=False)
    employee = relationship('Employee', back_populates='attendance')

    check_in_time = db.Column(db.DateTime)
    check_out_time = db.Column(db.DateTime)

    working_hours = db.Column(db.Double)

    date = db.Column(db.Date)

    IsCheckInRequest = db.Column(db.Boolean)
    IsCheckOutRequest = db.Column(db.Boolean)

    is_active = db.Column(db.Boolean)

    employee = relationship('Employee', back_populates='attendance')

    def __repr__(self):
        return f"<Attendance(id={self.id}, employee_id={self.employee_id}, date={self.date})>"

class SessionState(db.Model):
    __tablename__ = 'session_state'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_number = db.Column(db.String, nullable=False)
    session_key = db.Column(db.String, nullable=False)  # e.g., 'employee_identified', 'employee_id'
    session_value = db.Column(db.String, nullable=True)  # Store as string, convert as needed
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<SessionState(contact_number='{self.contact_number}', key='{self.session_key}', value='{self.session_value}')>"
    

