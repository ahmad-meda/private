from proxies.proxy import EmployeeProxy

class EmployeeChoices:

    @staticmethod
    def get_office_location_choices(group_id: int, company_id: int):
        return EmployeeProxy.get_companies_by_group_and_company(group_id=group_id, company_id=company_id)
    
    @staticmethod
    def get_role_choices():
        return EmployeeProxy.get_role_choices()

    @staticmethod
    def get_companies_choices(group_id: int, company_id: int):
        return EmployeeProxy.get_company_choices(group_id, company_id)
    
    @staticmethod
    def get_departments_choices():
        return EmployeeProxy.get_department_choices()
    
    @staticmethod
    def get_reporting_manager_choices(hr_company_id: int, hr_group_id: int):
        return EmployeeProxy.get_reporting_manager_choices(hr_company_id, hr_group_id)
    
    @staticmethod
    def get_work_policy_choices():
        return EmployeeProxy.get_work_policy_choices()
    
    @staticmethod
    def get_all_employee_names(hr_company_id: int = None, hr_group_id: int = None):
        return EmployeeProxy.get_all_employee_names(hr_company_id, hr_group_id)
    
    @staticmethod
    def get_gender_choices():
        return EmployeeProxy.get_gender_choices()
    