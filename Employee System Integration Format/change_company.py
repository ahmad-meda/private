from proxies.proxy import EmployeeProxy
# get employee for employee table:
def change_company(contact_number: str, company_name: str):
    employee_record = EmployeeProxy.get_employee_record(contact_number=contact_number)
    print(f"Employee Record: {employee_record}")

    #delete that record
    EmployeeProxy._soft_delete_employee(database_id=employee_record.id)

    print(f"Employee Record Deleted: {employee_record}")

    new_company_id = EmployeeProxy.get_company_id_by_name(company_name=company_name)

    #add new employee to database
    result = EmployeeProxy.add_employee_directly(
        employee_id=employee_record.employeeId,
        full_name=employee_record.name,
        contact_number=employee_record.contactNo,
        company_id=new_company_id,
        role_id=employee_record.role_id,
        work_policy_id=employee_record.work_policy_id,
        office_location_id=employee_record.office_location_id,
        department_id=employee_record.department_id,
        reporting_manager_id=employee_record.reporting_manager_id,
        first_name=employee_record.first_name,
        middle_name=employee_record.middle_name,
        last_name=employee_record.last_name,
        emailId=employee_record.emailId,
        designation=employee_record.designation,
        dateOfJoining=employee_record.dateOfJoining,
        dateOfBirth=employee_record.dateOfBirth,
        gender=employee_record.gender,
        home_latitude=employee_record.home_latitude,
        home_longitude=employee_record.home_longitude,
        allow_site_checkin=employee_record.allow_site_checkin,
        restrict_to_allowed_locations=employee_record.restrict_to_allowed_locations,
        reminders=employee_record.reminders,
        is_hr=employee_record.is_hr,
        hr_scope=employee_record.hr_scope,
        group_id=employee_record.group_id,
        created_by=employee_record.created_by
    )
    print(f"Result: {result}")

change_company(contact_number="+971509784398", company_name="Huse Test")