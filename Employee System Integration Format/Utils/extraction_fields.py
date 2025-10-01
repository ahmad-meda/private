from Files.SQLAlchemyModels import EmployeeDraft
from proxies.proxy import EmployeeProxy


def get_filled_fields(record_to_check: EmployeeDraft):
    company_name = None
    if record_to_check.company_id:
        company_obj = EmployeeProxy.get_company_by_id(record_to_check.company_id)
        company_name = company_obj.name if company_obj else None
    
    role_name = None
    if record_to_check.role_id:
        role_obj = EmployeeProxy.get_role_by_id(record_to_check.role_id)
        role_name = role_obj.name if role_obj else None
    
    office_location_name = None
    if record_to_check.office_location_id:
        office_obj = EmployeeProxy.get_office_location_by_id(record_to_check.office_location_id)
        office_location_name = office_obj.name if office_obj else None
    
    department_name = None
    if record_to_check.department_id:
        dept_obj = EmployeeProxy.get_department_by_id(record_to_check.department_id)
        department_name = dept_obj.name if dept_obj else None
    
    reporting_manager_name = None
    if record_to_check.reporting_manager_id:
        manager_obj = EmployeeProxy.get_reporting_manager_by_id(record_to_check.reporting_manager_id)
        reporting_manager_name = manager_obj.name if manager_obj else None
    
    filled_fields = {
        'full_name': record_to_check.name,
        'contact_number': record_to_check.contact_no,
        'emailId': record_to_check.email_id,
        'company_name': company_name,
        'role': role_name,
        'office_location_name': office_location_name,
        'department_name': department_name,
        'reporting_manager_name': reporting_manager_name,
        'designation': record_to_check.designation,
        'dateOfJoining': record_to_check.date_of_joining,
        'dateOfBirth': record_to_check.date_of_birth,
        'gender': record_to_check.gender,
        'reminders': record_to_check.reminders,
        'is_hr': record_to_check.is_hr,
        'hr_scope': record_to_check.hr_scope,
        'home_latitude': record_to_check.home_latitude,
        'home_longitude': record_to_check.home_longitude,
        'allow_site_checkin': record_to_check.allow_site_checkin,
        'restrict_to_allowed_locations': record_to_check.restrict_to_allowed_locations
    }
    
    return filled_fields