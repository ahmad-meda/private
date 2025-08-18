import re
from sqlalchemy.orm import Session, aliased
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from Files.SQLAlchemyModels import Attendance, Company, Department, Employee, Draft, Group, OfficeLocation, Role, WorkPolicy, EmployeeDraft
from datetime import datetime
from typing import Tuple, List, Optional, Dict, Any
from fuzzywuzzy import process
from sqlalchemy import and_
from Utils.fuzzy_logic import find_best_match
from Utils.fields_to_get import format_employee_details
from datetime import date
from sqlalchemy import func
from Utils.contact_validation import is_valid_international

class EmployeeService:

    @staticmethod
    def get_employee_record(contact_number: str, db_session: Session):
        #gets all the record of the employee based on their contact number
        contact_number = None if contact_number is None else re.sub(r'[^\d]', '', str(contact_number))
        try:
            employee = db_session.query(Employee).filter(
                Employee.contactNo == contact_number
            ).first()
            if employee is None:
                raise ValueError(f"No employee found with contact number: {contact_number}")
            return employee
        except Exception as e:
            raise Exception(f"Error retrieving employee by contact number {contact_number}: {str(e)}")
        
    @staticmethod
    def get_employee_record_by_name(name: str, db_session: Session):
        #gets all the record of the employee based on their name
        # Keep the name as text; only trim whitespace. Do not strip non-digits.
        name = None if name is None else str(name).strip()
        try:
            employee = db_session.query(Employee).filter(
                Employee.name == name
            ).first()
            if employee is None:
                raise ValueError(f"No employee found with name: {name}")
            return employee
        except Exception as e:
                raise Exception(f"Error retrieving employee by name {name}: {str(e)}")


    @staticmethod
    def get_hr_id_by_contact(contact_number: str, db_session) -> Tuple[int, str]:

        # clean the contact number by removing all non-digit characters
        contact_number = None if contact_number is None else re.sub(r'[^\d]', '', str(contact_number))
        print(f"Contact Number: {contact_number}")
        try:
            employee = db_session.query(Employee).filter(
                Employee.contactNo == contact_number
            ).first()
            if employee is None:
                raise ValueError(f"No employee found with contact number: {contact_number}")
            return employee.id, employee.name
        except Exception as e:
            raise Exception(f"Error retrieving employee by contact number {contact_number}: {str(e)}")
        
    @staticmethod
    def get_draft(employee_id: int, draft_type: str, db_session) -> Tuple[Draft, str, bool]:
    
        try:
            existing_draft = db_session.query(Draft).filter(
                Draft.employee_id == employee_id,
                Draft.draft_type == draft_type
            ).first()
            
            if existing_draft:
                return existing_draft.id, existing_draft.draft_id, True
            else:
                new_employee = EmployeeDraft()
                
                db_session.add(new_employee)
                db_session.flush() 
                
                new_draft = Draft(
                    employee_id=employee_id,
                    draft_type=draft_type,
                    draft_id=str(new_employee.id) )
                db_session.add(new_draft)
                db_session.commit()
                
                return new_draft.id, new_draft.draft_id, False
        except Exception as e:
            raise Exception(f"Error retrieving draft for employee {employee_id} with type {draft_type}: {str(e)}")
        

    @staticmethod
    def _add_created_by_to_employee_record(employee_record_id: int, hr_id: int, db: Session):
        try:
            draft = db.query(EmployeeDraft).filter(EmployeeDraft.id == employee_record_id).first()
            draft.created_by = hr_id
            db.commit()
        except Exception as e:
            raise Exception(f"Error adding created_by to draft for employee {employee_record_id}: {str(e)}")
        
    @staticmethod
    def get_all_employee_names(db: Session):
        try:
            names = db.query(Employee.name).filter(Employee.is_deleted == False).all()
            return [name[0] for name in names if name[0] not in (None, '')]
        
        except Exception as e:
            print(f"Error retrieving employee names: {e}")
            return []

    @staticmethod
    def get_role_choices(db: Session):
        roles = db.query(Role).all()
        return [role.name for role in roles]

    @staticmethod
    def get_company_choices(db: Session, group_id: int, company_id : int):
        # QUERY COMPANY BASED ON GROUP ID, IF THERE ARE NO COMPANIES BASED ON THE GIVEN GROUP ID THEN RETUEN AN EMTPY LIST
        if group_id is not None:
            companies = db.query(Company).filter(Company.group_id == group_id).all()
        else:
            companies = db.query(Company).filter(Company.id == company_id).all()
        if not companies:
            return []
        return [company.name for company in companies]

    @staticmethod
    def get_department_choices(db: Session):
        departments = db.query(Department).all()
        return [department.name for department in departments]

    @staticmethod
    def get_reporting_manager_choices(db: Session, hr_company_id: int, hr_group_id: int):
        if hr_group_id is not None:
            reporting_managers = db.query(Employee).filter(Employee.group_id == hr_group_id).all()
        else:
            reporting_managers = db.query(Employee).filter(Employee.company_id == hr_company_id).all()
        return [reporting_manager.name for reporting_manager in reporting_managers]

    @staticmethod
    def get_office_location_choices(db: Session):
        office_locations = db.query(OfficeLocation).all()
        return [office_location.name for office_location in office_locations]
    
    @staticmethod
    def get_group_choices(db: Session):
        groups = db.query(Group).all()
        return [group.name for group in groups]
    
    @staticmethod
    def get_work_policy_choices(db:Session):
        work_policies = db.query(WorkPolicy).all()
        return [work_policy.name for work_policy in work_policies]
    
    @staticmethod
    def get_gender_choices(db:Session):
        #null fields are not included
        genders = db.query(Employee).filter(Employee.gender.isnot(None)).all()
        return [gender.gender for gender in genders]
    
    @staticmethod
    def update_employee_company(employee_id: int, company_id: int, db:Session) -> Optional[int]:
        try:
            employee = db.query(EmployeeDraft).filter(EmployeeDraft.id == employee_id).first()
            employee.company_id = company_id
            company = db.query(Company).filter(Company.id == company_id).first()
            employee.employee_id = EmployeeService.generate_employee_identifier(db, company)
            db.commit()
            return employee.id if employee else None
        except Exception:
            return None
        
    
    @staticmethod
    def get_company_id_by_name(company_name: str, db:Session) -> Optional[int]:
        """Get company ID by name using SQLAlchemy ORM"""
        try:
            company = db.query(Company).filter(Company.name == company_name).first()
            return company.id if company else None
        except Exception:
            return None
        
    @staticmethod
    def get_role_id_by_name(role_name: str, db:Session) -> Optional[int]:
        """Get role ID by name using SQLAlchemy ORM"""
        try:
            role = db.query(Role).filter(Role.name == role_name).first()
            return role.id if role else None
        except Exception:
            return None
        
    @staticmethod
    def get_work_policy_id_by_name(policy_name: str, db:Session) -> Optional[int]:
        """Get work policy ID by name using SQLAlchemy ORM"""
        try:
            policy = db.query(WorkPolicy).filter(WorkPolicy.name == policy_name).first()
            return policy.id if policy else None
        except Exception:
            return None
        
    @staticmethod
    def get_office_location_id_by_name(location_name: str, db:Session) -> Optional[int]:
        """Get office location ID by name using SQLAlchemy ORM"""
        try:
            location = db.query(OfficeLocation).filter(OfficeLocation.name == location_name).first()
            return location.id if location else None
        except Exception:
            return None
        
    @staticmethod
    def get_department_id_by_name(department_name: str, db:Session) -> Optional[int]:
        """Get department ID by name using SQLAlchemy ORM"""
        try:
            department = db.query(Department).filter(Department.name == department_name).first()
            return department.id if department else None
        except Exception:
            return None
        
    @staticmethod
    def get_reporting_manager_id_by_name(manager_name: str, hr_company_id: int, hr_group_id: int, db:Session) -> Optional[int]:
        """Get reporting manager ID by name using SQLAlchemy ORM"""
        try:
            # if group id is not null, then filter by group id
            if hr_group_id is not None:
                manager = db.query(Employee).filter(Employee.name == manager_name, Employee.group_id == hr_group_id).first()
            else: # use company if grup is null
                manager = db.query(Employee).filter(Employee.name == manager_name, Employee.company_id == hr_company_id).first()
            return manager.id if manager else None
        except Exception:
            return None
        
    @staticmethod
    def _adding_new_employee(db_session: Session,
        employee_db_id: int,
        full_name: Optional[str] = None,
        contact_number: Optional[str] = None,
        company_name: Optional[str] = None,
        role: Optional[str] = None,
        work_policy_name: Optional[str] = None,
        office_location_name: Optional[str] = None,
        department_name: Optional[str] = None,
        reporting_manager_name: Optional[str] = None,
        first_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        last_name: Optional[str] = None,
        emailId: Optional[str] = None,
        designation: Optional[str] = None,
        dateOfJoining: Optional[str] = None,
        dateOfBirth: Optional[str] = None,
        gender: Optional[str] = None,
        home_latitude: Optional[float] = None,
        home_longitude: Optional[float] = None,
        allow_site_checkin: Optional[bool] = None,
        restrict_to_allowed_locations: Optional[bool] = None,
        reminders: Optional[bool] = None,
        is_hr: Optional[bool] = None, # this is for the employee being added is an HR
        hr_scope: Optional[str] = None,
        hr_company_id: int = None,
        hr_group_id: int = None
        ) -> Dict[str, Any]:

        error_dict = {}
    
        try:
            # Get the employee record
            employee_draft = db_session.query(EmployeeDraft).filter(EmployeeDraft.id == employee_db_id).first()
            if not employee_draft:
                error_dict['employee'] = 'Employee not found'
                return {'success': False, 'errors': error_dict}
            
            # Check for duplicate email (if emailId is being updated)
            if emailId is not None and emailId != employee_draft.email_id:
                # Check in Employee table
                existing_email = db_session.query(Employee).filter(
                    Employee.emailId == emailId,
                    Employee.is_deleted == False
                ).first()
                
                if existing_email:
                    emailId = None  
                    error_dict['emailId'] = 'Email already exists for another employee'
            
            # Check for duplicate contact number (if contact_number is being updated) and clean it
            if contact_number is not None and contact_number != employee_draft.contact_no:
                contact_number = None if contact_number is None else re.sub(r'[^\d]', '', str(contact_number))
                
                # Check in Employee table
                existing_contact = db_session.query(Employee).filter(
                    Employee.contactNo == contact_number,
                    Employee.is_deleted == False
                ).first()
                
                print(f"Existing Contact: {existing_contact}")
                
                if existing_contact:
                    #fix this
                    contact_number = None  # Set to None to prevent duplicate
                    error_dict['contact_number'] = 'Contact number already exists for another employee'
                correct_format = is_valid_international(contact_number)
                if correct_format is False:
                    contact_number = None
                    error_dict['contact_number'] = 'Invalid contact number format, the length or the country code is invalid'
            
            # Look up related entities and validate they exist using existing static methods
            company_id = None
            if company_name is not None:
                company_id = EmployeeService.get_company_id_by_name(company_name, db_session)

                if company_id is None:
                    error_dict['company_name'] = 'Company not found, please clarify. present choices to user. here are the options: ' + ', '.join(EmployeeService.get_company_choices(db_session, hr_group_id, hr_company_id))
                elif company_id is not None:
                    # Get company details to fetch prefix
                    company = db_session.query(Company).filter(Company.id == company_id).first()
                    if company:
                        #add group is the company is in a group
                        group_id = None
                        if company.group_id is not None:
                            group_id = company.group_id
                        if group_id is not None:
                            employee_draft.group_id = group_id
                        
                        # Only generate employee_id if we have a valid company
                        generated_id = EmployeeService.generate_employee_identifier(db_session, company)
                        if generated_id is not None:
                            employee_draft.employee_id = generated_id
                        else:
                            error_dict['company_name'] = 'Failed to generate employee identifier'
                    else:
                        error_dict['company_name'] = 'Company not found, please clarify. present choices to user. here are the options: ' + ', '.join(EmployeeService.get_company_choices(db_session, hr_group_id, hr_company_id))
            
            role_id = None
            if role is not None:
                role_id = EmployeeService.get_role_id_by_name(role, db_session)
                if role_id is None:
                    
                    error_dict['role'] = 'Role not found, please clarify. present choices to user. here are the options: ' + ', '.join(EmployeeService.get_role_choices(db_session))
            
            work_policy_id = None
            if work_policy_name is not None:
                work_policy_id = EmployeeService.get_work_policy_id_by_name(work_policy_name, db_session)
                if work_policy_id is None:
                    
                    error_dict['work_policy_name'] = 'Work policy not found, please clarify. present choices to user. here are the options: ' + ', '.join(EmployeeService.get_work_policy_choices(db_session))
            
            office_location_id = None
            if office_location_name is not None or office_location_name != 'manager_skip' or office_location_name != 'home_coordinates':
                office_location_id = EmployeeService.get_office_location_id_by_name(office_location_name, db_session)
                if office_location_id is None:
                  
                    error_dict['office_location_name'] = 'Office location not found,Please clarify.present choices to user. here are the options: ' + ', '.join(EmployeeService.get_companies_by_group_and_company(db_session, hr_group_id, hr_company_id))
            
            department_id = None
            if department_name is not None:
                department_id = EmployeeService.get_department_id_by_name(department_name, db_session)
                if department_id is None:
                  
                    error_dict['department_name'] = 'Department not found, please clarify. present choices to user. here are the options: ' + ', '.join(EmployeeService.get_department_choices(db_session))
            
            reporting_manager_id = None
            if reporting_manager_name is not None:
                reporting_manager_id = EmployeeService.get_reporting_manager_id_by_name(reporting_manager_name, hr_company_id, hr_group_id, db_session)
                if reporting_manager_id is None:
                
                    error_dict['reporting_manager_name'] = 'Reporting manager not found'
            
            # Parse and validate dates
            date_of_joining = None
            if dateOfJoining is not None:
                try:
                    date_of_joining = datetime.strptime(dateOfJoining, '%Y-%m-%d').date()
                except ValueError:
                    dateOfJoining = None
                    error_dict['dateOfJoining'] = 'Invalid date format. Use YYYY-MM-DD'
            
            date_of_birth = None
            if dateOfBirth is not None:
                try:
                    date_of_birth = datetime.strptime(dateOfBirth, '%Y-%m-%d').date()
                except ValueError:
                    dateOfBirth = None
                    error_dict['dateOfBirth'] = 'Invalid date format. Use YYYY-MM-DD'

            if allow_site_checkin is not None:
                employee_draft.allow_site_checkin = allow_site_checkin
            if restrict_to_allowed_locations is not None:
                employee_draft.restrict_to_allowed_locations = restrict_to_allowed_locations
            
            # Update the employee record with provided values
            if full_name is not None:
                employee_draft.name = full_name
            if contact_number is not None:
                employee_draft.contact_no = contact_number
            if first_name is not None:
                employee_draft.first_name = first_name
            if middle_name is not None:
                employee_draft.middle_name = middle_name
            if last_name is not None:
                employee_draft.last_name = last_name
            if emailId is not None:
                employee_draft.email_id = emailId
            if designation is not None:
                employee_draft.designation = designation
            if gender is not None:
                employee_draft.gender = gender
            if home_latitude is not None:
                employee_draft.home_latitude = str(home_latitude)
            if home_longitude is not None:
                employee_draft.home_longitude = str(home_longitude)
            if allow_site_checkin is not None:
                employee_draft.allow_site_checkin = allow_site_checkin
            if restrict_to_allowed_locations is not None:
                employee_draft.restrict_to_allowed_locations = restrict_to_allowed_locations
            if reminders is not None:
                employee_draft.reminders = reminders
            if is_hr is not None:
                employee_draft.is_hr = is_hr
            if hr_scope is not None:
                employee_draft.hr_scope = hr_scope
            # Update foreign key references
            if company_id is not None:
                employee_draft.company_id = company_id
            if role_id is not None:
                employee_draft.role_id = role_id
            if work_policy_id is not None:
                employee_draft.work_policy_id = work_policy_id
            if office_location_id is not None:
                employee_draft.office_location_id = office_location_id
            if department_id is not None:
                employee_draft.department_id = department_id
            if reporting_manager_id is not None:
                employee_draft.reporting_manager_id = reporting_manager_id
            
            # Update dates
            if date_of_joining is not None:
                employee_draft.date_of_joining = date_of_joining
            if date_of_birth is not None:
                employee_draft.date_of_birth = date_of_birth

            # Commit the changes
            db_session.commit()

            # If there are any validation errors, return them
            if error_dict:
                return {'success': False, 'errors': error_dict}
            
            
            return {'success': True, 'errors': error_dict}
            
        except IntegrityError as e:
            db_session.rollback()
            error_dict['database'] = 'Database integrity error occurred'
            return {'success': False, 'errors': error_dict}
        
        except Exception as e:
            db_session.rollback()
            error_dict['general'] = f'An unexpected error occurred: {str(e)}'
            return {'success': False, 'errors': error_dict}

    @staticmethod
    def _add_employee_in_main_database(draft_id: int, db_session: Session) -> Dict[str, Any]:
        try:
            # Fetch the draft row
            draft_employee = db_session.query(EmployeeDraft).filter(EmployeeDraft.id == draft_id).one()

            # Create an Employee object, copying fields except 'id'
            new_employee = Employee(
                employeeId=draft_employee.employee_id,
                first_name=draft_employee.first_name,
                middle_name=draft_employee.middle_name,
                last_name=draft_employee.last_name,
                name=draft_employee.name,
                emailId=draft_employee.email_id,
                designation=draft_employee.designation,
                dateOfJoining=draft_employee.date_of_joining,
                dateOfBirth=draft_employee.date_of_birth,
                contactNo=draft_employee.contact_no,
                gender=draft_employee.gender,
                office_location_id=draft_employee.office_location_id,
                work_policy_id=draft_employee.work_policy_id,
                home_latitude=draft_employee.home_latitude,
                home_longitude=draft_employee.home_longitude,
                company_id=draft_employee.company_id,
                group_id=draft_employee.group_id,
                reporting_manager_id=draft_employee.reporting_manager_id,
                role_id=draft_employee.role_id,
                department_id=draft_employee.department_id,
                is_hr=draft_employee.is_hr,
                hr_scope=draft_employee.hr_scope,
                allow_site_checkin=draft_employee.allow_site_checkin,
                restrict_to_allowed_locations=draft_employee.restrict_to_allowed_locations,
                reminders=draft_employee.reminders,
                is_deleted=draft_employee.is_deleted,
                deleted_at=draft_employee.deleted_at
                # Related entities like leave_requests, attendance, etc. are not copied by default.
            )

            db_session.add(new_employee)
            db_session.commit()

            return {"message": "Draft published successfully", "new_employee_id": new_employee.id}

        except Exception as e:
            db_session.rollback()
            return {"error": str(e)}        
       
        
    @staticmethod
    def _update_employee_by_id(db_session: Session,
        employee_db_id: int,
        full_name: Optional[str] = None,
        contact_number: Optional[str] = None,
        company_name: Optional[str] = None,
        role: Optional[str] = None,
        work_policy_name: Optional[str] = None,
        office_location_name: Optional[str] = None,
        department_name: Optional[str] = None,
        reporting_manager_name: Optional[str] = None,
        first_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        last_name: Optional[str] = None,
        emailId: Optional[str] = None,
        designation: Optional[str] = None,
        dateOfJoining: Optional[str] = None,
        dateOfBirth: Optional[str] = None,
        gender: Optional[str] = None,
        home_latitude: Optional[float] = None,
        home_longitude: Optional[float] = None,
        allow_site_checkin: Optional[bool] = None,
        restrict_to_allowed_locations: Optional[bool] = None,
        reminders: Optional[bool] = None,
        is_hr: Optional[bool] = None, # this is for the employee being added is an HR
        hr_scope: Optional[str] = None,
        hr_company_id: int = None,
        hr_group_id: int = None
        ) -> Dict[str, Any]:
        """
        Updates an employee record by database ID and returns error dictionary if validation fails.
        
        Returns:
            Dict containing 'success' boolean and 'errors' dict with field-specific error messages
        """
        
        error_dict = {}
    
        try:

            # FIXED : CANNOT UPDATE DELETED EMPLOYEES
            # Get the employee record
            employee = db_session.query(Employee).filter(
                Employee.id == employee_db_id,
                Employee.is_deleted == False
            ).first()
            if not employee:
                error_dict['employee'] = 'Employee not found or has been deleted'
                return {'success': False, 'errors': error_dict}
            
            # Check for duplicate email (if emailId is being updated)
            if emailId is not None and emailId != employee.emailId:
                existing_email = db_session.query(Employee).filter(
                    Employee.emailId == emailId,
                    Employee.id != employee_db_id,
                    Employee.is_deleted == False
                ).first()
                if existing_email:
                    emailId = None
                    error_dict['emailId'] = 'Email already exists for another employee'
            
            # Validate then check duplicate for contact number (if being updated)
            if contact_number is not None and contact_number != employee.contactNo:
                cleaned_contact = re.sub(r'[^\d]', '', str(contact_number))

                # Validate format first
                if not cleaned_contact or is_valid_international(cleaned_contact) is False:
                    contact_number = None
                    error_dict['contact_number'] = 'Invalid contact number format, the length or the country code is invalid'
                else:
                    # Check for duplicate only if valid
                    existing_contact = db_session.query(Employee).filter(
                        Employee.contactNo == cleaned_contact,
                        Employee.id != employee_db_id,
                        Employee.is_deleted == False
                    ).first()
                    if existing_contact:
                        contact_number = None
                        error_dict['contact_number'] = 'Contact number already exists for another employee'
                    else:
                        contact_number = cleaned_contact
            
            # Look up related entities and validate they exist using existing static methods
            company_id = None
            if company_name is not None:
                company_id = EmployeeService.get_company_id_by_name(company_name, db_session)

                if company_id is None:
                    error_dict['company_name'] = 'Company not found, please clarify. present choices to user. here are the options: ' + ', '.join(EmployeeService.get_company_choices(db_session, hr_group_id, hr_company_id))
                elif company_id is not None:
                    # Get company details to fetch prefix
                    company = db_session.query(Company).filter(Company.id == company_id).first()
                    if company:
                        #add group is the company is in a group
                        group_id = None
                        if company.group_id is not None:
                            group_id = company.group_id
                        if group_id is not None:
                            employee.group_id = group_id
                        
                        # Only generate employee_id if we have a valid company
                        generated_id = EmployeeService.generate_employee_identifier(db_session, company)
                        if generated_id is not None:
                            employee.employeeId = generated_id
                        else:
                            error_dict['company_name'] = 'Failed to generate employee identifier'
                    else:
                        error_dict['company_name'] = 'Company not found'
                    
            
            role_id = None
            if role is not None:
                role_id = EmployeeService.get_role_id_by_name(role, db_session)
                if role_id is None:
                    error_dict['role'] = 'Role not found'
            
            work_policy_id = None
            if work_policy_name is not None:
                work_policy_id = EmployeeService.get_work_policy_id_by_name(work_policy_name, db_session)
                if work_policy_id is None:
                    error_dict['work_policy_name'] = 'Work policy not found'
            
            office_location_id = None
            if office_location_name is not None:
                office_location_id = EmployeeService.get_office_location_id_by_name(office_location_name, db_session)
                if office_location_id is None:
                    error_dict['office_location_name'] = 'Office location not found,Please clarify.present choices to user. here are the options: ' + ', '.join(EmployeeService.get_companies_by_group_and_company(db_session, hr_group_id, hr_company_id))
            
            department_id = None
            if department_name is not None:
                department_id = EmployeeService.get_department_id_by_name(department_name, db_session)
                if department_id is None:
                    error_dict['department_name'] = 'Department not found'
            
            reporting_manager_id = None
            if reporting_manager_name is not None:
                reporting_manager_id = EmployeeService.get_reporting_manager_id_by_name(reporting_manager_name, hr_company_id, hr_group_id, db_session)
                if reporting_manager_id is None:
                    error_dict['reporting_manager_name'] = 'Reporting manager not found'
            
            # Parse and validate dates
            date_of_joining = None
            if dateOfJoining is not None:
                try:
                    date_of_joining = datetime.strptime(dateOfJoining, '%Y-%m-%d').date()
                except ValueError:
                    error_dict['dateOfJoining'] = 'Invalid date format. Use YYYY-MM-DD'
            
            date_of_birth = None
            if dateOfBirth is not None:
                try:
                    date_of_birth = datetime.strptime(dateOfBirth, '%Y-%m-%d').date()
                except ValueError:
                    error_dict['dateOfBirth'] = 'Invalid date format. Use YYYY-MM-DD'

            if allow_site_checkin is not None:
                employee.allow_site_checkin = allow_site_checkin
            if restrict_to_allowed_locations is not None:
                employee.restrict_to_allowed_locations = restrict_to_allowed_locations
            if reminders is not None:
                employee.reminders = reminders
            # If there are any validation errors, return them
            if error_dict:
                return {'success': False, 'errors': error_dict}
            
            # Update the employee record with provided values
            if full_name is not None:
                employee.name = full_name
            if contact_number is not None:
                employee.contactNo = contact_number
            if first_name is not None:
                employee.first_name = first_name
            if middle_name is not None:
                employee.middle_name = middle_name
            if last_name is not None:
                employee.last_name = last_name
            if emailId is not None:
                employee.emailId = emailId
            if designation is not None:
                employee.designation = designation
            if gender is not None:
                employee.gender = gender
            if home_latitude is not None:
                employee.home_latitude = str(home_latitude)
            if home_longitude is not None:
                employee.home_longitude = str(home_longitude)
            if allow_site_checkin is not None:
                employee.allow_site_checkin = allow_site_checkin
            if restrict_to_allowed_locations is not None:
                employee.restrict_to_allowed_locations = restrict_to_allowed_locations
            if reminders is not None:
                employee.reminders = reminders
            if is_hr is not None:
                employee.is_hr = is_hr
            if hr_scope is not None:
                employee.hr_scope = hr_scope
            
            # Update foreign key references
            if company_id is not None:
                employee.company_id = company_id
            if role_id is not None:
                employee.role_id = role_id
            if work_policy_id is not None:
                employee.work_policy_id = work_policy_id
            if office_location_id is not None:
                employee.office_location_id = office_location_id
            if department_id is not None:
                employee.department_id = department_id
            if reporting_manager_id is not None:
                employee.reporting_manager_id = reporting_manager_id
            
            # Update dates
            if date_of_joining is not None:
                employee.dateOfJoining = date_of_joining
            if date_of_birth is not None:
                employee.dateOfBirth = date_of_birth
            
            # Commit the changes
            db_session.commit()
            
            return {'success': True, 'errors': {}}
            
        except IntegrityError as e:
            db_session.rollback()
            error_dict['database'] = 'Database integrity error occurred'
            return {'success': False, 'errors': error_dict}
        
        except Exception as e:
            db_session.rollback()
            error_dict['general'] = f'An unexpected error occurred: {str(e)}'
            return {'success': False, 'errors': error_dict}

    @staticmethod
    def get_filled_fields(database_id, db_session: Session):
    
        try:
            employee = db_session.query(Employee).filter(Employee.id == database_id).first()
            if not employee:
                return None
            
            result = {}
            for column in Employee.__table__.columns:
                value = getattr(employee, column.name)
                if value is not None and value != '':
                    result[column.name] = value
            
            return result
            
        except Exception as e:
            raise e
        finally:
            db_session.close()

    @staticmethod
    def get_null_fields(database_id, db_session: Session):
    
        try:
            employee = db_session.query(EmployeeDraft).filter(EmployeeDraft.id == database_id).first()
            if not employee:
                return None
            
            result = {}
            for column in EmployeeDraft.__table__.columns:
                value = getattr(employee, column.name)
                # Normalize empty strings to None for consistency
                if value == '':
                    value = None
                    
                if value is None:
                    if column.name == 'name':
                        key = 'full_name'
                    elif column.name == 'company_id':
                        key = 'company_name'
                    elif column.name == 'contact_no':
                        key = 'contact_number'
                    elif column.name == 'email_id':
                        key = 'emailId'
                    elif column.name == 'role_id':
                        key = 'role'
                    elif column.name == 'work_policy_id':
                        key = 'work_policy_name'
                    elif column.name == 'office_location_id':
                        key = 'office_location_name'
                    elif column.name == 'department_id':
                        key = 'department_name'
                    elif column.name == 'reporting_manager_id':
                        key = 'reporting_manager_name'
                    elif column.name == "date_of_birth":
                        key = "dateOfBirth"
                    elif column.name == "date_of_joining":
                        key = "dateOfJoining"
                    else:
                        key = column.name
                    result[key] = value
            
            return result

        except Exception as e:
            raise e
        finally:
            db_session.close()

    @staticmethod
    def get_employee_id_by_contact(contactno: str, db_session: Session, hr_group_id: Optional[int] = None, hr_company_id: Optional[int] = None):
        response = {
        "success": False,
        "database_id": None,
        "error": None
    }
        # clean the contact number by removing all non-digit characters
        contactno = None if contactno is None else re.sub(r'[^\d]', '', str(contactno))
        try:
            cleaned_contact = str(contactno).strip()

            # Filter employees: prefer group when provided, otherwise by company
            query = db_session.query(Employee).filter(Employee.is_deleted == False)
            if hr_group_id is not None:
                query = query.filter(Employee.group_id == hr_group_id)
            elif hr_company_id is not None:
                query = query.filter(Employee.company_id == hr_company_id)

            # Execute the built query
            employees = query.all()

            for emp in employees:
                if emp.contactNo:
                    db_contact = str(emp.contactNo).strip()
                    if db_contact == cleaned_contact:
                        response["success"] = True
                        response["database_id"] = emp.id
                        return response

            response["error"] = f"No employee found with contact number '{contactno}'."
            return response

        except SQLAlchemyError as e:
            response["error"] = f"Database error: {str(e)}"
            return response

        except Exception as e:
            response["error"] = f"Unexpected error: {str(e)}"
            return response

    @staticmethod
    def get_employee_id_by_name(name: str, email: Optional[str], contact_number: Optional[str], hr_group_id: Optional[int], hr_company_id: Optional[int], db_session: Session):
       
        response = {
            "success": False,
            "database_id": None,
            "error": None,
            "matches": []
        }

        try:
            # Filter employees: prefer group when provided, otherwise by company
            query = db_session.query(Employee).filter(Employee.is_deleted == False)
            if hr_group_id is not None:
                query = query.filter(Employee.group_id == hr_group_id)
            elif hr_company_id is not None:
                query = query.filter(Employee.company_id == hr_company_id)

            employees = query.all()
            employee_data = [
                {
                    "name": emp.name,
                    "database_id": emp.id,
                    "email": emp.emailId,   
                    "contactno": emp.contactNo
                }
                for emp in employees if emp.name
            ]

            # Use fuzzy matching to find the best matches
            choices = [emp["name"] for emp in employee_data]
            matches = process.extract(name, choices, limit=5)

            # Filter matches with a high score (adjust threshold if needed)
            high_score_matches = [match for match in matches if match[1] >= 100]

            if not high_score_matches:
                response["error"] = f"No employee found matching '{name}'."
                return response

            if len(high_score_matches) > 1:
                # Ambiguous match, get all matching employees
                matched_names = [m[0] for m in high_score_matches]
                
                multiple_employees = [
                    {
                        "name": emp["name"],
                        "email": emp["email"],
                        "contactno": emp["contactno"],
                        "database_id": emp["database_id"]
                    }
                    for emp in employee_data if emp["name"] in matched_names
                ]
                
                # Try to narrow down using additional details if provided
                if email and email.strip():
                    # Check if any of the multiple employees match the provided email
                    email_matches = [emp for emp in multiple_employees if emp["email"] and emp["email"].lower() == email.lower().strip()]
                    if len(email_matches) == 1:
                        # Found exact match using email
                        response["success"] = True
                        response["database_id"] = email_matches[0]["database_id"]
                        return response
                
                if contact_number and contact_number.strip():
                    # Clean contact number (remove non-digits)
                    clean_contact = ''.join(filter(str.isdigit, contact_number))
                    # Check if any of the multiple employees match the provided contact
                    contact_matches = [emp for emp in multiple_employees if emp["contactno"] and ''.join(filter(str.isdigit, emp["contactno"])) == clean_contact]
                    if len(contact_matches) == 1:
                        # Found exact match using contact number
                        response["success"] = True
                        response["database_id"] = contact_matches[0]["database_id"]
                        return response
                
                # If additional details don't help narrow down, return multiple options
                response["error"] = {
                    "message": f"Multiple employees found matching '{name}'. Please clarify.present choices to user along with their mentioned details.",
                    "multiple_employees": multiple_employees
                }
                return response

            # Single clear match
            matched_name = high_score_matches[0][0]
            matched_employee = next(emp for emp in employee_data if emp["name"] == matched_name)

            response["success"] = True
            response["database_id"] = matched_employee["database_id"]
            return response

        except SQLAlchemyError as e:
            response["error"] = f"Database error: {str(e)}"
            return response

        except Exception as e:
            response["error"] = f"Unexpected error: {str(e)}"
            return response
        
    @staticmethod
    def _delete_draft(draft_id, db: Session):   

        try:
            draft = db.query(Draft).filter(Draft.id == draft_id).first()
            if draft:
                db.delete(draft)
                db.commit()
                return True
            else:
                return False
                
        except Exception as e:
            db.rollback()
            print(f"Error deleting draft: {e}")
            raise e
        finally:
            db.close()

    @staticmethod
    def _soft_delete_employee(database_id: int, db: Session):
        try:
            # if employee in the same group can be deleted, then delete the employee
           # if group is null hen employee can be deleted only based on the same company
           
            employee = db.query(Employee).filter(Employee.id == database_id).first()        
            #if employee is already deleted, then return False  
            if employee.is_deleted:
                return False
            employee.is_deleted = True
            employee.deleted_at = datetime.now()
            db.commit()
            return True
        
        except Exception as e:
            db.rollback()
            return None
        

    #---- Get Operation Functions ----

    @staticmethod
    def get_employees_by_company(company:str, db:Session):

        try:
            company = db.query(Company).filter(Company.name == company).first()
            
            if not company:
                return [], {"error": f"No company found with name '{company}'"}
            
            employees = db.query(Employee).filter(
                Employee.company_id == company.id,
                Employee.is_deleted == False
            ).all()
            
            # Convert each employee to dictionary with all fields
            employee_list = []
            for emp in employees:
                emp_dict = {}
                for column in emp.__table__.columns:
                    if column.name not in ['id', 'deleted_at', 'is_deleted']:
                        value = getattr(emp, column.name)
                        # Convert datetime to string if needed
                        if hasattr(value, 'isoformat'):
                            value = str(value)
                        emp_dict[column.name] = value
                employee_list.append(emp_dict)
            
            return employee_list, {}
        
        except Exception as e:
            return [], {"error": str(e)}
    
    @staticmethod
    def get_employees_by_reporting_manager(reporting_manager:str, db:Session):
        
        try:
            manager = db.query(Employee).filter(Employee.name == reporting_manager, Employee.is_deleted == False).first()
            
            if not manager:
                return [], {"error": f"No manager found with name '{reporting_manager}'"}
            
            employees = db.query(Employee).filter(
                Employee.reporting_manager_id == manager.id,
                Employee.is_deleted == False
            ).all()
            
            # Convert each employee to dictionary with all fields
            employee_list = []
            for emp in employees:
                emp_dict = {}
                for column in emp.__table__.columns:
                    if column.name not in ['id', 'deleted_at', 'is_deleted']:
                        value = getattr(emp, column.name)
                        # Convert datetime to string if needed
                        if hasattr(value, 'isoformat'):
                            value = str(value)
                        emp_dict[column.name] = value
                employee_list.append(emp_dict)
            
            return employee_list, {}
        
        except Exception as e:
            return [], {"error": str(e)}
    
    @staticmethod
    def get_online_employees(db: Session):

        try:
                online_attendance_records = db.query(Attendance).filter(
                    and_(
                        Attendance.check_in_time.isnot(None),
                        Attendance.check_out_time.is_(None),
                    )
                ).all()
                
                # Convert each online employee to dictionary with all fields
                employee_list = []
                for record in online_attendance_records:
                    emp = record.employee
                    if emp and not emp.is_deleted:  # Only active employees
                        emp_dict = {}
                        for column in emp.__table__.columns:
                            if column.name not in ['id', 'deleted_at', 'is_deleted']:
                                value = getattr(emp, column.name)
                                # Convert datetime to string if needed
                                if hasattr(value, 'isoformat'):
                                    value = str(value)
                                emp_dict[column.name] = value
                        employee_list.append(emp_dict)
                
                return employee_list, {}
            
        except Exception as e:
                return [], {"error": str(e)}
        
    @staticmethod
    def get_employees_by_office_location(office: str, db: Session):
        try:
            employees = db.query(Employee).join(
                OfficeLocation, Employee.office_location_id == OfficeLocation.id
            ).filter(
                OfficeLocation.name == office,
                Employee.is_deleted == False
            ).all()
            
            # Convert each employee to dictionary with all fields
            employee_list = []
            for emp in employees:
                emp_dict = {}
                for column in emp.__table__.columns:
                    if column.name not in ['id', 'deleted_at', 'is_deleted']:
                        value = getattr(emp, column.name)
                        # Convert datetime to string if needed
                        if hasattr(value, 'isoformat'):
                            value = str(value)
                        emp_dict[column.name] = value
                employee_list.append(emp_dict)
            
            return employee_list, {}
    
        except Exception as e:
            return [], {"error": str(e)}

    @staticmethod
    def get_contact_by_role(role: str, db: Session):
        try:
            role_obj = db.query(Role).filter(Role.name == role).first()
            
            if not role_obj:
                return [], {"error": f"No role found with name '{role}'"}

            employees = db.query(Employee).filter(
                Employee.role_id == role_obj.id,
                Employee.is_deleted == False
            ).all()

            # Convert each employee to dictionary with all fields
            employee_list = []
            for emp in employees:
                if emp.contactNo:  # Only include employees with contact numbers
                    emp_dict = {}
                    for column in emp.__table__.columns:
                        if column.name not in ['id', 'deleted_at', 'is_deleted']:
                            value = getattr(emp, column.name)
                            # Convert datetime to string if needed
                            if hasattr(value, 'isoformat'):
                                value = str(value)
                            emp_dict[column.name] = value
                    employee_list.append(emp_dict)

            return employee_list, {}
        
        except Exception as e:
            return [], {"error": str(e)}
    
    @staticmethod
    def get_employees_by_department(department: str, db: Session):
        try:
            employees = db.query(Employee).join(
                Department, Employee.department_id == Department.id
            ).filter(
                Department.name == department,
                Employee.is_deleted == False
            ).all()
            
            # Convert each employee to dictionary with all fields
            employee_list = []
            for emp in employees:
                emp_dict = {}
                for column in emp.__table__.columns:
                    if column.name not in ['id', 'deleted_at', 'is_deleted']:
                        value = getattr(emp, column.name)
                        # Convert datetime to string if needed
                        if hasattr(value, 'isoformat'):
                            value = str(value)
                        emp_dict[column.name] = value
                employee_list.append(emp_dict)
            
            return employee_list, {}
        
        except Exception as e:
            return [], {"error": str(e)}
        
    @staticmethod
    def get_employees_by_gender(gender: str, db: Session):
        try:
            employees = db.query(Employee).filter(
                Employee.gender == gender,
                Employee.is_deleted == False
            ).all()
            
            # Convert each employee to dictionary with all fields
            employee_list = []
            for emp in employees:
                emp_dict = {}
                for column in emp.__table__.columns:
                    if column.name not in ['id', 'deleted_at', 'is_deleted']:
                        value = getattr(emp, column.name)
                        # Convert datetime to string if needed
                        if hasattr(value, 'isoformat'):
                            value = str(value)
                        emp_dict[column.name] = value
                employee_list.append(emp_dict)
            
            return employee_list, {}
        
        except Exception as e:
            return [], {"error": str(e)}
        

    @staticmethod
    def generate_employee_identifier(session: Session, company: Company) -> str:
        """
        Build an employeeId like:
          {PREFIX}{COMPANY_ID}{SEQ}

        - PREFIX: first letters of each word in company.name (2 chars), uppercased
        - COMPANY_ID: 3-digit, zero-padded company.id
        - SEQ:       4-digit, zero-padded count of existing employees + 1

        e.g. company "Blue Sky" id=5, first hire => BS0050001
        """
        # 1) PREFIX from company name
        #    take initials; if only one word, use its first two letters
        try:
            # Handle None or empty company name
            if not company or not company.name or company.name.strip() == "":
                raise ValueError("Company name is empty or None")
                
            company_name = company.name.strip()
            words = re.findall(r"\b\w", company_name)
            if len(words) >= 2:
                prefix = (words[0] + words[1]).upper()
            else:
                prefix = company_name[:2].upper()

            # 2) COMPANY_ID zero-padded
            comp_id = str(company.id).zfill(3)

            # 3) SEQ = count of existing + 1
            existing = session.query(Employee).filter_by(company_id=company.id).count()
            seq = existing + 1
            seq_str = str(seq).zfill(4)

            return f"{prefix}{comp_id}{seq_str}"
        except Exception as e:
            print(f"Error generating employee identifier: {e}")
            # Return None or raise the exception instead of returning nothing
            return None

#--------------------------------------------GET OPERATIONS--------------------------------------------
    @staticmethod
    def get_employee_by_name(db: Session, name: str, hr_company_id: int = None, group_id: int = None):
        name = find_best_match(name, EmployeeService.get_all_employee_names(db), threshold=95)
        try:
            query = db.query(Employee).filter(
                Employee.name.ilike(f"%{name}%"),
                Employee.is_deleted == False
            )
            if group_id:
                query = query.filter(Employee.group_id == group_id)
            elif hr_company_id:
                query = query.filter(Employee.company_id == hr_company_id)
                
            employee = query.first()
            if not employee:
                return "", {"error": f"Employee '{name}' not found."}
            
            return format_employee_details(employee), {}
        except Exception as e:
            return "", {"error": str(e)}

    @staticmethod
    def get_employee_by_employee_id(db: Session, employee_id: str, hr_company_id: int = None, group_id: int = None):
        try:
            query = db.query(Employee).filter(
                Employee.employeeId == employee_id,
                Employee.is_deleted == False
            )
            
            if group_id:
                query = query.filter(Employee.group_id == group_id)
            elif hr_company_id:
                query = query.filter(Employee.company_id == hr_company_id)
                
            employee = query.first()
            if not employee:
                return "", {"error": f"Employee with ID '{employee_id}' not found."}
            
            return format_employee_details(employee), {}
        except Exception as e:
            return "", {"error": str(e)}

    @staticmethod
    def get_employee_by_email(db: Session, email: str, hr_company_id: int = None, group_id: int = None):
        try:
            query = db.query(Employee).filter(
                Employee.emailId.ilike(f"%{email}%"),
                Employee.is_deleted == False
            )
            if group_id:
                query = query.filter(Employee.group_id == group_id)
            elif hr_company_id:
                query = query.filter(Employee.company_id == hr_company_id)
                
            employee = query.first()
            if not employee:
                return "", {"error": f"Employee with email '{email}' not found."}
            
            return format_employee_details(employee), {}
        except Exception as e:
            return "", {"error": str(e)}
    
    @staticmethod
    def get_employee_by_contact_number(db: Session, contact_number: str, hr_company_id: int = None, group_id: int = None):
        try:
            contact_number = None if contact_number is None else re.sub(r'[^\d]', '', str(contact_number))
            query = db.query(Employee).filter(
                Employee.contactNo == contact_number,
                Employee.is_deleted == False
            )
            if group_id:
                query = query.filter(Employee.group_id == group_id)
            elif hr_company_id:
                query = query.filter(Employee.company_id == hr_company_id)
                
            employee = query.first()
            if not employee:
                return "", {"error": f"Employee with contact number '{contact_number}' not found."}
            
            return format_employee_details(employee), {}
        except Exception as e:
            return "", {"error": str(e)}
        
    @staticmethod
    def get_employee_by_date_of_joining(db: Session, date_of_joining: str, hr_company_id: int = None, group_id: int = None):
        try:
            query = db.query(Employee).filter(
                Employee.dateOfJoining == date_of_joining,
                Employee.is_deleted == False
            )
            if group_id:
                query = query.filter(Employee.group_id == group_id)
            elif hr_company_id:   
                query = query.filter(Employee.company_id == hr_company_id)
                
            employees = query.all()
            if not employees:
                return "", {"error": f"No employees found with date of joining '{date_of_joining}'."}
            
            result = f"Employees with date of joining '{date_of_joining}':\n\n"
            for emp in employees:
                result += format_employee_details(emp) + "\n" + "-"*50 + "\n"
            return result, {}
        except Exception as e:
            return "", {"error": str(e)}
        
    @staticmethod
    def get_employee_by_date_of_birth(db: Session, date_of_birth: str, hr_company_id: int = None, group_id: int = None):
        try:
            query = db.query(Employee).filter(
                Employee.dateOfBirth == date_of_birth,
                Employee.is_deleted == False
            )
            if group_id:
                query = query.filter(Employee.group_id == group_id)
            elif hr_company_id:
                query = query.filter(Employee.company_id == hr_company_id)
                
            employees = query.all()
            if not employees:
                return "", {"error": f"No employees found with date of birth '{date_of_birth}'."}
            
            result = f"Employees with date of birth '{date_of_birth}':\n\n"
            for emp in employees:
                result += format_employee_details(emp) + "\n" + "-"*50 + "\n"
            return result, {}
        except Exception as e:
            return "", {"error": str(e)}

        
    
    @staticmethod
    def get_employee_by_gender(db: Session, gender: str, hr_company_id: int = None, group_id: int = None):
        gender = find_best_match(gender, EmployeeService.get_gender_choices(db), threshold=90)
        try:
            query = db.query(Employee).filter(
                Employee.gender == gender,
                Employee.is_deleted == False
            )
            if group_id:
                query = query.filter(Employee.group_id == group_id)
            elif hr_company_id:
                query = query.filter(Employee.company_id == hr_company_id)

            employees = query.all()
            if not employees:
                return "", {"error": f"No employees found with gender '{gender}'."}
            
            result = f"Employees with gender '{gender}':\n\n"
            for emp in employees:   
                result += format_employee_details(emp) + "\n" + "-"*50 + "\n"
            return result, {}
        except Exception as e:
            return "", {"error": str(e)}

    @staticmethod
    def get_employee_by_designation(db: Session, designation: str, hr_company_id: int = None, group_id: int = None):
        try:
            query = db.query(Employee).filter(
                Employee.designation.ilike(f"%{designation}%"),
                Employee.is_deleted == False
            )
            if group_id:
                query = query.filter(Employee.group_id == group_id)
            elif hr_company_id:
                query = query.filter(Employee.company_id == hr_company_id)
                
            employees = query.all()
            if not employees:
                return "", {"error": f"No employees found with designation '{designation}'."}
            
            result = f"Employees with designation '{designation}':\n\n"
            for emp in employees:
                result += format_employee_details(emp) + "\n" + "-"*50 + "\n"
            return result, {}
        except Exception as e:
            return "", {"error": str(e)}

    @staticmethod
    def get_employee_by_department(db: Session, department_name: str, hr_company_id: int = None, group_id: int = None):
        try:
            department_name = find_best_match(department_name, EmployeeService.get_department_choices(db), threshold=85)
            department_id = EmployeeService.get_department_id_by_name(department_name, db)
            if not department_id:
                return "", {"error": f"Department '{department_name}' not found."}
                
            query = db.query(Employee).filter(
                Employee.department_id == department_id,
                Employee.is_deleted == False
            )
            if group_id:
                query = query.filter(Employee.group_id == group_id)
            elif hr_company_id:
                query = query.filter(Employee.company_id == hr_company_id)
                
            employees = query.all()
            if not employees:
                return "", {"error": f"No employees found in department '{department_name}'."}
            
            result = f"Employees in {department_name} department:\n\n"
            for emp in employees:
                result += format_employee_details(emp) + "\n" + "-"*50 + "\n"
            return result, {}
        except Exception as e:
            return "", {"error": str(e)}

    @staticmethod
    def get_employee_by_company(db: Session, company_name: str, hr_company_id: int = None, group_id: int = None):
        try:
            company_name = find_best_match(company_name, EmployeeService.get_company_choices(db, group_id, hr_company_id), threshold=85)
            company_id = EmployeeService.get_company_id_by_name(company_name, db)
            if not company_id:
                return "", {"error": f"Company '{company_name}' not found."}
                
            employees = db.query(Employee).filter(
                Employee.company_id == company_id,
                Employee.is_deleted == False
            ).all()
            if not employees:
                return "", {"error": f"No employees found in company '{company_name}'."}
            
            result = f"Employees in {company_name}:\n\n"
            for emp in employees:
                result += format_employee_details(emp) + "\n" + "-"*50 + "\n"
            return result, {}
        except Exception as e:
            return "", {"error": str(e)}

    @staticmethod
    def get_employee_by_office_location(db: Session, location_name: str, hr_company_id: int = None, group_id: int = None):
        try:
            location_name = find_best_match(location_name, EmployeeService.get_office_location_choices(db), threshold=85)
            location_id = EmployeeService.get_office_location_id_by_name(location_name, db)
            if not location_id:
                return "", {"error": f"Office location '{location_name}' not found."}
                
            employees = db.query(Employee).filter(
                Employee.office_location_id == location_id,
                Employee.is_deleted == False
            ).all()
            if not employees:
                return "", {"error": f"No employees found in office location '{location_name}'."}
            
            result = f"Employees in {location_name} office:\n\n"
            for emp in employees:
                result += format_employee_details(emp) + "\n" + "-"*50 + "\n"
            return result, {}
        except Exception as e:
            return "", {"error": str(e)}

    @staticmethod
    def get_employee_by_reporting_manager(db: Session, manager_name: str, hr_company_id: int = None, group_id: int = None):
        try:
            manager_name = find_best_match(manager_name, EmployeeService.get_reporting_manager_choices(db, hr_company_id, group_id), threshold=85)
            manager_id = EmployeeService.get_reporting_manager_id_by_name(manager_name, hr_company_id, group_id, db)
            if not manager_id:
                return "", {"error": f"Reporting manager '{manager_name}' not found."}
                
            employees = db.query(Employee).filter(
                Employee.reporting_manager_id == manager_id,
                Employee.is_deleted == False
            ).all()
            if not employees:
                return "", {"error": f"No employees found reporting to '{manager_name}'."}
            
            result = f"Employees reporting to {manager_name}:\n\n"
            for emp in employees:
                result += format_employee_details(emp) + "\n" + "-"*50 + "\n"
            return result, {}
        except Exception as e:
            return "", {"error": str(e)}
    
    @staticmethod
    def get_employee_by_role(db: Session, role_name: str, hr_company_id: int = None, group_id: int = None):
        try:
            role_name = find_best_match(role_name, EmployeeService.get_role_choices(db), threshold=85)
            print(f"Role Name: {role_name}")
            role_id = EmployeeService.get_role_id_by_name(role_name, db)
            if not role_id:
                return "", {"error": f"Role '{role_name}' not found."}
                
            query = db.query(Employee).filter(
                Employee.role_id == role_id,
                Employee.is_deleted == False
            )
            if group_id:
                query = query.filter(Employee.group_id == group_id)
            elif hr_company_id:
                query = query.filter(Employee.company_id == hr_company_id)
                
            employees = query.all()
            if not employees:
                return "", {"error": f"No employees found with role '{role_name}'."}
            
            result = f"Employees with role '{role_name}':\n\n"
            for emp in employees:
                result += format_employee_details(emp) + "\n" + "-"*50 + "\n"
            return result, {}
        except Exception as e:
            return "", {"error": str(e)}
    
    @staticmethod
    def get_checked_in_employee_ids(db: Session, hr_company_id: int, group_id: int = None):
        """
        Get IDs of employees who are currently checked in (online) for a specific company
        
        Args:
            db: Database session
            hr_company_id: Company ID to filter employees
        
        Returns:
            list: List of employee IDs who are checked in
        """
        try:
            today = date.today()
            
            # Query attendance records for employees who are checked in (online)
            online_attendance_records = db.query(Attendance).join(Employee).filter(
                and_(
                    Attendance.check_in_time.isnot(None),
                    Attendance.check_out_time.is_(None),
                    Attendance.is_active == True,
                    func.date(Attendance.check_in_time) == today,
                    Employee.company_id == hr_company_id,
                    Employee.is_deleted == False
                )
            ).all()
            
            # Extract employee IDs
            employee_ids = []
            for record in online_attendance_records:
                if record.employee:
                    employee_ids.append(record.employee.id)
            
            return employee_ids
            
        except Exception as e:
            return []

    @staticmethod
    def get_checked_in_employees(db: Session, hr_company_id: int, group_id: int = None):
        """
        Get all employees who are currently checked in (online) for a specific company
        
        Args:
            db: Database session
            hr_company_id: Company ID to filter employees
        
        Returns:
            tuple: (result_string, error_dict)
        """
        try:
            employee_ids = EmployeeService.get_checked_in_employee_ids(db, hr_company_id)
            
            if not employee_ids:
                return "", {"error": "No employees are currently checked in."}
            
            # Get employee objects and format results
            employees = db.query(Employee).filter(Employee.id.in_(employee_ids)).all()
            result = f"Employees currently checked in (online):\n\n"
            
            for emp in employees:
                result += format_employee_details(emp) + "\n" + "="*50 + "\n"
            
            return result, {}
            
        except Exception as e:
            return "", {"error": str(e)}
        

        
#--------------------------------------------BUILDING THE MAIN GET EMPLOYEE FUNCTION--------------------------------------------

    
    @staticmethod
    def get_employee_by_criteria(db: Session, criteria_list: list, hr_company_id: int, group_id: int = None):
        """
        Get employees based on multiple criteria
        
        Args:
            db: Database session
            criteria_list: List of tuples in format [("field", "value"), ("field", "value"), ...]
            hr_company_id: Company ID to filter employees
        
        Returns:
            tuple: (result_string, error_dict)
        """
        try:
            if not criteria_list:
                return "", {"error": "No criteria provided."}
            
            # Start with all employees from the group or company
            query = db.query(Employee).filter(
                Employee.is_deleted == False
            )
            
            if group_id:
                query = query.filter(Employee.group_id == group_id)
            else:
                query = query.filter(Employee.company_id == hr_company_id)
            
            # Apply each criteria
            for field, value in criteria_list:
                if field == "name":
                    # Use fuzzy matching for name
                    matched_name = find_best_match(value, EmployeeService.get_all_employee_names(db), threshold=95)
                    query = query.filter(Employee.name.ilike(f"%{matched_name}%"))
                    
                elif field == "employeeId":
                    query = query.filter(Employee.employeeId == value)
                    
                elif field == "emailId":
                    query = query.filter(Employee.emailId.ilike(f"%{value}%"))
                    
                elif field == "contactNo":
                    contact_number = None if value is None else re.sub(r'[^\d]', '', str(value))
                    query = query.filter(Employee.contactNo == contact_number)
                    
                elif field == "gender":
                    matched_gender = find_best_match(value, EmployeeService.get_gender_choices(db), threshold=90)
                    query = query.filter(Employee.gender == matched_gender)
                    
                elif field == "designation":
                    query = query.filter(Employee.designation.ilike(f"%{value}%"))

                elif field == "company_name":
                    matched_company = find_best_match(value, EmployeeService.get_company_choices(db, group_id, hr_company_id), threshold=85)
                    company_id = EmployeeService.get_company_id_by_name(matched_company, db)
                    if not company_id:
                        return "", {"error": f"Company '{value}' not found."}
                    query = query.filter(Employee.company_id == company_id)
                    
                elif field == "department_name":
                    matched_dept = find_best_match(value, EmployeeService.get_department_choices(db), threshold=85)
                    dept_id = EmployeeService.get_department_id_by_name(matched_dept, db)
                    if not dept_id:
                        return "", {"error": f"Department '{value}' not found."}
                    query = query.filter(Employee.department_id == dept_id)

                elif field == "dateOfJoining":
                    # Validate date first
                    if not value:
                        return "", {"error": "Date of joining is required."}
                    try:
                        # Validate date format
                        parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
                        query = query.filter(Employee.dateOfJoining == parsed_date)
                    except ValueError:
                        return "", {"error": "Invalid date format. Please use YYYY-MM-DD."}

                elif field == "dateOfBirth":
                    # Validate date first
                    if not value:
                        return "", {"error": "Date of birth is required."}
                    try:
                        # Validate date format
                        parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
                        query = query.filter(Employee.dateOfBirth == parsed_date)
                    except ValueError:
                        return "", {"error": "Invalid date format. Please use YYYY-MM-DD."}
                    
                elif field == "office_location_name":
                    matched_location = find_best_match(value, EmployeeService.get_office_location_choices(db), threshold=85)
                    location_id = EmployeeService.get_office_location_id_by_name(matched_location, db)
                    if not location_id:
                        return "", {"error": f"Office location '{value}' not found."}
                    query = query.filter(Employee.office_location_id == location_id)
                    
                elif field == "reporting_manager_name":
                    matched_manager = find_best_match(value, EmployeeService.get_reporting_manager_choices(db, hr_company_id, group_id), threshold=85)
                    manager_id = EmployeeService.get_reporting_manager_id_by_name(matched_manager, hr_company_id, group_id, db)
                    if not manager_id:
                        return "", {"error": f"Reporting manager '{value}' not found."}
                    query = query.filter(Employee.reporting_manager_id == manager_id)
                    
                elif field == "role_name":
                    matched_role = find_best_match(value, EmployeeService.get_role_choices(db), threshold=85)
                    role_id = EmployeeService.get_role_id_by_name(matched_role, db)
                    if not role_id:
                        return "", {"error": f"Role '{value}' not found."}
                    query = query.filter(Employee.role_id == role_id)

                elif field == "checked_in":
                    # Always return employees who are currently checked in, ignore value
                    checked_in_employee_ids = EmployeeService.get_checked_in_employee_ids(db, hr_company_id, group_id)
                    if checked_in_employee_ids:
                        query = query.filter(Employee.id.in_(checked_in_employee_ids))
                    else:
                        # No checked-in employees, return empty result
                        return "", {"error": "No employees are currently checked in."}
                    
                    
                else:
                    return "", {"error": f"Unsupported criteria field: '{field}'"}
            
            # Execute query
            employees = query.all()
            
            if not employees:
                criteria_str = ", ".join([f"{field}='{value}'" for field, value in criteria_list])
                return "", {"error": f"No employees found matching criteria: {criteria_str}"}
            
            # Format results
            criteria_description = ", ".join([f"{field}: '{value}'" for field, value in criteria_list])
            result = []
            
            for emp in employees:
                emp_details = format_employee_details(emp)
                result.extend(emp_details)  # Use extend to flatten the list: ["string1", "string2"]

            print(result)
                
            return result, {}
            
        except Exception as e:
            return "", {"error": str(e)}
        
    @staticmethod
    def get_companies_by_group_and_company(db: Session, group_id: Optional[int], company_id: int) -> List[str]:
        if group_id is not None:
            # Filter by both group and company
            offices = db.query(OfficeLocation).join(Company).filter(
                Company.group_id == group_id,
                Company.id == company_id,
                OfficeLocation.is_active == True
            ).all()
        else:
            # Filter by company only
            offices = db.query(OfficeLocation).filter(
                OfficeLocation.company_id == company_id,
                OfficeLocation.is_active == True
            ).all()
        
        return [o.name for o in offices]
            
