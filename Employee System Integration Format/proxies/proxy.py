from typing import List, Tuple, Optional
from services.service import EmployeeService

class EmployeeProxy:

    @staticmethod
    def get_company_by_id(company_id):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_company_by_id(db.session, company_id)
    
    @staticmethod
    def get_role_by_id(role_id):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_role_by_id(db.session, role_id)
    
    @staticmethod
    def get_work_policy_by_id(work_policy_id):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_work_policy_by_id(db.session, work_policy_id)
    
    @staticmethod
    def get_office_location_by_id(office_location_id):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_office_location_by_id(db.session, office_location_id)
    
    @staticmethod
    def get_department_by_id(department_id):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_department_by_id(db.session, department_id)
    
    @staticmethod
    def get_reporting_manager_by_id(reporting_manager_id):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_reporting_manager_by_id(db.session, reporting_manager_id)
    
    @staticmethod
    def get_group_by_id(group_id):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_group_by_id(db.session, group_id)

    @staticmethod
    def get_employee_draft_record_by_id(employee_id):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_draft_record_by_id(employee_id, db.session)

    @staticmethod
    def get_employee_record_by_id(employee_id):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_record_by_id(employee_id, db.session)

    @staticmethod
    def get_employee_record(contact_number: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_record(contact_number, db.session)
        

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
    def get_all_employee_names(hr_company_id: int = None, hr_group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_all_employee_names(db.session, hr_company_id, hr_group_id)
    
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
    def get_company_id_by_name(company_name: str, hr_group_id: int = None, hr_company_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_company_id_by_name(company_name, db.session, hr_group_id, hr_company_id)
    
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
    def get_group_id_by_name(name: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_group_id_by_name(name, db.session)
    
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
                               is_hr: bool,
                               hr_scope: str,
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
                                                      is_hr, hr_scope,
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
    def get_employee_by_name(name: str, hr_company_id: int = None, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_name(db.session, name, hr_company_id, group_id)
        
    @staticmethod
    def get_employee_by_employee_id(employee_id: str, hr_company_id: int = None, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_employee_id(employee_id, db.session, group_id)
        
    @staticmethod
    def get_employee_by_email(email: str, hr_company_id: int = None, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_email(db.session, email, group_id)
        
    @staticmethod   
    def get_employee_by_contact_number(contact_number: str, hr_company_id: int = None, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_contact_number(db.session, contact_number, hr_company_id, group_id)
        
    @staticmethod
    def get_employee_by_gender(gender: str, hr_company_id: int = None, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_gender(db.session, gender, hr_company_id, group_id)
        
    @staticmethod
    def get_employee_by_designation(designation: str, hr_company_id: int = None, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_designation(db.session, designation, hr_company_id, group_id)
        
    @staticmethod
    def get_employee_by_department(department: str, hr_company_id: int = None, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_department(db.session, department, hr_company_id, group_id)
        
    @staticmethod
    def get_employee_by_company(company: str, hr_company_id: int = None, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_company(db.session, company, hr_company_id, group_id)
        
    @staticmethod
    def get_employee_by_office_location(office: str, hr_company_id: int = None, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_office_location(db.session, office, hr_company_id, group_id)
        
    @staticmethod
    def get_employee_by_reporting_manager(reporting_manager: str, hr_company_id: int = None, group_id: int = None):  
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_reporting_manager(db.session, reporting_manager, hr_company_id, group_id)
        
    @staticmethod
    def get_employee_by_role(role: str, hr_company_id: int = None, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_by_role(db.session, role, hr_company_id, group_id)
    
    @staticmethod
    def get_checked_in_employees(hr_company_id: int, group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_checked_in_employees(db.session, hr_company_id, group_id)
        
    @staticmethod
    def get_office_locations_by_group_and_company(group_id: int, company_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_office_locations_by_group_and_company(db.session, group_id, company_id)
        
    @staticmethod
    def save_employee_office_locations(employee_id: int, office_location_names: list):
        from app import app, db
        with app.app_context():
            return EmployeeService.save_employee_office_locations(employee_id, office_location_names, db.session)
        
    @staticmethod
    def create_leave_balances_for_employee(employee_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService.create_leave_balances_for_employee(employee_id, db.session)
        
    @staticmethod
    def check_username_exists(username: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.check_username_exists(db.session, username)
        
    @staticmethod
    def check_password_exists(password: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.check_password_exists(db.session, password)
        
    @staticmethod
    def add_employee_to_huse(employee_id: int, huse_app_id: int, app_username: str, app_password: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.add_employee_to_huse(employee_id, huse_app_id, app_username, app_password, db.session)
        
    @staticmethod
    def get_employee_record_by_name(name: str, hr_company_id: int = None, hr_group_id: int = None):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_record_by_name(db.session, name, hr_company_id, hr_group_id)
    
    @staticmethod
    def get_company_by_name(name: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_company_by_name(db.session, name)
        
    @staticmethod
    def save_office_locations_to_employee(employee_id: int, office_location_ids: list):
        from app import app, db
        with app.app_context():
            return EmployeeService.save_office_locations_to_employee(employee_id, office_location_ids, db.session)
        
    @staticmethod
    def add_lead(full_legal_name: Optional[str] = None,
                 preferred_nickname: Optional[str] = None,
                 date_of_birth: Optional[str] = None,
                 nationality: Optional[str] = None,
                 phone_number: Optional[str] = None,
                 email_address: Optional[str] = None,
                 suggested_membership_tier: Optional[str] = None,
                 residential_address: Optional[str] = None,
                 passport_number: Optional[str] = None,
                 id_number: Optional[str] = None,
                 occupation: Optional[str] = None,
                 job_title: Optional[str] = None, 
                 linkedin_or_website: Optional[str] = None,
                 education_background: Optional[str] = None,
                 notable_affiliations: Optional[str] = None,
                 lead_comments: Optional[str] = None,
                 conversion_status: Optional[str] = None,
                 approval_status: Optional[str] = None,
                 lead_status: Optional[str] = None,
                 company: Optional[str] = None,
                 agent_id: Optional[str] = None,
                 crm_backend_id: Optional[str] = None,
                 status : Optional[str] = None,):
        """
        Proxy function to add a lead.
        """
        from app import app, db
        with app.app_context():
            return EmployeeService.add_lead(db=db.session, full_legal_name=full_legal_name, 
                                        preferred_nickname=preferred_nickname, 
                                        date_of_birth=date_of_birth, 
                                        nationality=nationality, 
                                        phone_number=phone_number, 
                                        email_address=email_address, 
                                        suggested_membership_tier=suggested_membership_tier, 
                                        residential_address=residential_address, 
                                        passport_number=passport_number, 
                                        id_number=id_number, 
                                        occupation=occupation, 
                                        job_title=job_title, 
                                        linkedin_or_website=linkedin_or_website, 
                                        education_background=education_background, 
                                        notable_affiliations=notable_affiliations, 
                                        lead_comments=lead_comments, 
                                        conversion_status=conversion_status, 
                                        approval_status=approval_status, 
                                        lead_status=lead_status, 
                                        company=company, 
                                        agent_id=agent_id, 
                                        crm_backend_id=crm_backend_id, 
                                        status=status)
        


    @staticmethod
    def get_all_active_employees():
        from app import app, db
        with app.app_context():
            return EmployeeService.get_all_active_employees(db.session)
        
    @staticmethod
    def update_employee_credentials(employee_id: int, username: str, password: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.update_employee_credentials(db.session, employee_id, username, password) 
    
    @staticmethod
    def get_all_employees_by_company(company_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_all_employees_by_company(db.session, company_id)
        
    @staticmethod
    def get_all_employees_by_group(group_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_all_employees_by_group(db.session, group_id)
    
    @staticmethod
    def get_all_employees_by_company_list(company_list: list[int]):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_all_employees_by_company_list(db.session, company_list)
        
    @staticmethod
    def get_all_usernames():
        from app import app, db
        with app.app_context():
            return EmployeeService.get_all_usernames(db.session)
        
    @staticmethod
    def clear_employee_draft_fields(draft_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService.clear_employee_draft_fields(draft_id, db.session)
        
    @staticmethod
    def get_lead_record(lead_id: int):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_lead_record(db.session, lead_id)
   