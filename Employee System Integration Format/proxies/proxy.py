from typing import List, Tuple
from services.service import EmployeeService

class EmployeeProxy:

    @staticmethod
    def get_employee_record(contact_number: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_record(contact_number, db.session)
        
    @staticmethod
    def get_employee_record_by_name(name: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_record_by_name(name, db.session)

    @staticmethod
    def get_hr_id_by_contact(contact_number: str) -> int:
        from app import app, db
        with app.app_context():
            return EmployeeService.get_hr_id_by_contact(contact_number, db.session)
    
    @staticmethod
    def get_draft(employee_id: int, draft_type: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_draft(employee_id, draft_type, db.session)
        
    @staticmethod
    def _add_created_by_to_employee_record(employee_record_id: int, hr_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService._add_created_by_to_employee_record(employee_record_id, hr_id, db.session)
    
    @staticmethod
    def get_all_employee_names():
        from app import app, db
        with app.app_context():
            return EmployeeService.get_all_employee_names(db.session)
    
    @staticmethod
    def get_role_choices():
        from app import app, db
        with app.app_context():
            return EmployeeService.get_role_choices(db.session)
    
    @staticmethod
    def get_company_choices(group_id: int, company_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_company_choices(db.session, group_id, company_id)
    
    @staticmethod
    def get_reporting_manager_choices(hr_company_id: int, hr_group_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_reporting_manager_choices(db.session, hr_company_id, hr_group_id)
    
    @staticmethod
    def get_group_choices():
        from app import app, db
        with app.app_context():
            return EmployeeService.get_group_choices(db.session)
    
    @staticmethod
    def get_department_choices():
        from app import app, db
        with app.app_context():
            return EmployeeService.get_department_choices(db.session)
    
    @staticmethod
    def get_office_location_choices():
        from app import app, db
        with app.app_context():
            return EmployeeService.get_office_location_choices(db.session)

    @staticmethod
    def get_work_policy_choices():
        from app import app, db
        with app.app_context():
            return EmployeeService.get_work_policy_choices(db.session)
    
    @staticmethod
    def get_gender_choices():
        from app import app, db
        with app.app_context():
            return EmployeeService.get_gender_choices(db.session)
        
    @staticmethod
    def update_employee_company(employee_id: int, company_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService.update_employee_company(employee_id, company_id, db.session)
    
    @staticmethod
    def get_company_id_by_name(company_name: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_company_id_by_name(company_name, db.session)
    
    @staticmethod
    def get_role_id_by_name(role_name: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_role_id_by_name(role_name, db.session)
    
    @staticmethod
    def get_work_policy_id_by_name(work_policy_name: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_work_policy_id_by_name(work_policy_name, db.session)
    
    @staticmethod
    def get_office_location_id_by_name(office_location_name: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_office_location_id_by_name(office_location_name, db.session)
    
    @staticmethod
    def get_department_id_by_name(department_name: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_department_id_by_name(department_name, db.session)
    
    @staticmethod
    def get_reporting_manager_id_by_name(reporting_manager_name: str, hr_company_id: int = None, hr_group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_reporting_manager_id_by_name(reporting_manager_name, hr_company_id, hr_group_id, db.session)
    
    @staticmethod
    def _adding_new_employee(employee_db_id: int,
                            full_name: str, 
                            contact_number: str, 
                            company_name: str, 
                            role: str, 
                            work_policy_name: str, 
                            office_location_name: str, 
                            department_name: str, 
                            reporting_manager_name: str, 
                            first_name: str, 
                            middle_name: str, 
                            last_name: str, 
                            emailId: str, 
                            designation: str, 
                            dateOfJoining: str, 
                            dateOfBirth: str, 
                            gender: str, 
                            home_latitude: float, 
                            home_longitude: float,
                            allow_site_checkin: bool,
                            restrict_to_allowed_locations: bool,
                            reminders: bool,
                            is_hr: bool,
                            hr_scope: str,
                            hr_company_id: int,
                            hr_group_id: int,
                            ):
        from app import app, db
        with app.app_context():
            return EmployeeService._adding_new_employee(db.session, 
                                                      employee_db_id, 
                                                      full_name, contact_number, 
                                                      company_name, role, 
                                                      work_policy_name, 
                                                      office_location_name, 
                                                      department_name, 
                                                      reporting_manager_name, 
                                                      first_name, middle_name, 
                                                      last_name, emailId, 
                                                      designation, dateOfJoining, 
                                                      dateOfBirth, gender, 
                                                      home_latitude, home_longitude,
                                                      allow_site_checkin, restrict_to_allowed_locations,
                                                      reminders,
                                                      is_hr, hr_scope,
                                                      hr_company_id, hr_group_id)
    @staticmethod
    def _add_employee_in_main_database(draft_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService._add_employee_in_main_database(draft_id, db.session)

    @staticmethod
    def _update_employee_by_id(employee_db_id: int, 
                               full_name: str, 
                               contact_number: str, 
                               company_name: str, 
                               role: str, 
                               work_policy_name: str, 
                               office_location_name: str, 
                               department_name: str, 
                               reporting_manager_name: str, 
                               first_name: str, 
                               middle_name: str, 
                               last_name: str, 
                               emailId: str, 
                               designation: str, 
                               dateOfJoining: str, 
                               dateOfBirth: str, 
                               gender: str, 
                               home_latitude: float, 
                               home_longitude: float,
                               allow_site_checkin: bool,
                               restrict_to_allowed_locations: bool,
                               reminders: bool,
                               hr_company_id: int,
                               hr_group_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService._update_employee_by_id(db.session, 
                                                      employee_db_id, 
                                                      full_name, contact_number, 
                                                      company_name, role, 
                                                      work_policy_name, 
                                                      office_location_name, 
                                                      department_name, 
                                                      reporting_manager_name, 
                                                      first_name, middle_name, 
                                                      last_name, emailId, 
                                                      designation, dateOfJoining, 
                                                      dateOfBirth, gender, 
                                                      home_latitude, home_longitude,
                                                      allow_site_checkin, restrict_to_allowed_locations,
                                                      reminders,
                                                      hr_company_id, hr_group_id)
    
    @staticmethod
    def get_filled_fields(employee_db_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_filled_fields(employee_db_id, db.session)

    @staticmethod
    def get_null_fields(employee_db_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_null_fields(employee_db_id, db.session)
    
    @staticmethod
    def get_employee_id_by_contact(contact_number: str, hr_group_id: int = None, hr_company_id: int = None  ):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_id_by_contact(contact_number, db.session, hr_group_id, hr_company_id)
    
    @staticmethod
    def get_employee_id_by_name(name: str, email: str = None, contact_number: str = None, hr_group_id: int = None, hr_company_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_id_by_name(name, email, contact_number, hr_group_id, hr_company_id, db.session)
    
    @staticmethod
    def _delete_draft(draft_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService._delete_draft(draft_id, db.session)
    
    @staticmethod
    def _soft_delete_employee(database_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService._soft_delete_employee(database_id, db.session)
    
    @staticmethod
    def get_employees_by_company(company:str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employees_by_company(company, db.session)
    
    @staticmethod
    def get_employees_by_reporting_manager(reporting_manager:str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employees_by_reporting_manager(reporting_manager, db.session)    
    
    @staticmethod
    def get_contact_by_role(role:str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_contact_by_role(role, db.session)
    
    @staticmethod
    def get_online_employees():
        from app import app, db
        with app.app_context():
            return EmployeeService.get_online_employees(db.session)
    
    @staticmethod
    def get_employees_by_department(department:str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employees_by_department(department, db.session)
    
    @staticmethod
    def get_employees_by_gender(gender:str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employees_by_gender(gender, db.session)
    
    @staticmethod
    def get_employees_by_office_location(office:str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employees_by_office_location(office, db.session)     
        
    @staticmethod
    def get_employee_by_criteria(criteria_list: list[tuple[str, str]], hr_company_id: int, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_criteria(db.session, criteria_list, hr_company_id, group_id)
        
    @staticmethod
    def get_employee_by_name(name: str, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_name(db.session, name, group_id)
        
    @staticmethod
    def get_employee_by_employee_id(employee_id: str, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_employee_id(employee_id, db.session, group_id)
        
    @staticmethod
    def get_employee_by_email(email: str, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_email(db.session, email, group_id)
        
    @staticmethod   
    def get_employee_by_contact_number(contact_number: str, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_contact_number(db.session, contact_number, group_id)
        
    @staticmethod
    def get_employee_by_gender(gender: str, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_gender(db.session, gender, group_id)
        
    @staticmethod
    def get_employee_by_designation(designation: str, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_designation(db.session, designation, group_id)
        
    @staticmethod
    def get_employee_by_department(department: str, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_department(db.session, department, group_id)
        
    @staticmethod
    def get_employee_by_company(company: str, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_company(db.session, company, group_id)
        
    @staticmethod
    def get_employee_by_office_location(office: str, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_office_location(db.session, office, group_id)
        
    @staticmethod
    def get_employee_by_reporting_manager(reporting_manager: str, group_id: int = None):  
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_reporting_manager(db.session, reporting_manager, group_id)
        
    @staticmethod
    def get_employee_by_role(role: str, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_role(db.session, role, group_id)
    
    @staticmethod
    def get_checked_in_employees(hr_company_id: int, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_checked_in_employees(db.session, hr_company_id, group_id)
        
    @staticmethod
    def get_companies_by_group_and_company(group_id: int, company_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_companies_by_group_and_company(db.session, group_id, company_id)
        
