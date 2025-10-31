import os
from typing import Dict, Any
from proxies.proxy import EmployeeProxy


def user_by_username(username: str, company_name: str = None, group_name: str = None) -> Dict[str, Any]:
    """
    Get employee record by username from the database with company/group filtering
    
    Args:
        username: The username to search for
        company_name: Optional company name for filtering
        group_name: Optional group name for filtering
        
    Returns:
        Dictionary containing success status and employee data or error message
        
    Note:
        - If group_name is provided, filter by group
        - If group_name is None but company_name is provided, filter by company
        - At least one of group_name or company_name must be provided
    """
    try:
        # Validation: Check if username is provided
        if not username:
            return {
                'success': False,
                'error': 'Username is required'
            }
        
        # Validation: Strip whitespace
        username = username.strip()
        
        # Validation: Check if username is not empty after stripping
        if not username:
            return {
                'success': False,
                'error': 'Username cannot be empty or whitespace only'
            }
        
        # Validation: Check if username length is reasonable
        if len(username) < 3:
            return {
                'success': False,
                'error': 'Username must be at least 3 characters long'
            }
        
        if len(username) > 50:
            return {
                'success': False,
                'error': 'Username cannot exceed 50 characters'
            }
        
        # Validation: Check if at least one filter is provided
        if not group_name and not company_name:
            return {
                'success': False,
                'error': 'Either group_name or company_name must be provided for filtering'
            }
        
        # Convert names to IDs for efficient database filtering
        company_id = None
        group_id = None
        
        if group_name:
            group_id = EmployeeProxy.get_group_id_by_name(group_name)
            if not group_id:
                return {
                    'success': False,
                    'error': f'Group "{group_name}" not found',
                    'group_name': group_name
                }
        elif company_name:
            company_id = EmployeeProxy.get_company_id(company_name)
            if not company_id:
                return {
                    'success': False,
                    'error': f'Company "{company_name}" not found',
                    'company_name': company_name
                }
        
        # Get employee from database with efficient filtering
        employee = EmployeeProxy.get_employee_by_username(username, company_id=company_id, group_id=group_id)
        
        # Check if employee was found
        if not employee:
            return {
                'success': False,
                'error': f'Employee with username "{username}" not found',
                'username': username
            }
        
        # Get related entity names
        company_name = None
        if employee.company_id:
            company = EmployeeProxy.get_company_by_id(employee.company_id)
            company_name = company.name if company else None
        
        role_name = None
        if employee.role_id:
            role = EmployeeProxy.get_role_by_id(employee.role_id)
            role_name = role.name if role else None
        
        department_name = None
        if employee.department_id:
            department = EmployeeProxy.get_department_by_id(employee.department_id)
            department_name = department.name if department else None
        
        group_name = None
        if employee.group_id:
            group = EmployeeProxy.get_group_by_id(employee.group_id)
            group_name = group.name if group else None
        
        reporting_manager_name = None
        if employee.reporting_manager_id:
            reporting_manager = EmployeeProxy.get_reporting_manager_by_id(employee.reporting_manager_id)
            reporting_manager_name = reporting_manager.name if reporting_manager else None
        
        office_location_name = None
        if employee.office_location_id:
            office_location = EmployeeProxy.get_office_location_by_id(employee.office_location_id)
            office_location_name = office_location.name if office_location else None
        
        work_policy_name = None
        if employee.work_policy_id:
            work_policy = EmployeeProxy.get_work_policy_by_id(employee.work_policy_id)
            work_policy_name = work_policy.name if work_policy else None
        
        # Convert employee object to dictionary for response
        employee_data = {
            'id': employee.id,
            'employeeId': employee.employeeId,
            'first_name': employee.first_name,
            'middle_name': employee.middle_name,
            'last_name': employee.last_name,
            'name': employee.name,
            'emailId': employee.emailId,
            'designation': employee.designation,
            'dateOfJoining': employee.dateOfJoining.isoformat() if employee.dateOfJoining else None,
            'dateOfBirth': employee.dateOfBirth.isoformat() if employee.dateOfBirth else None,
            'contactNo': employee.contactNo,
            'gender': employee.gender,
            'username': employee.username,
            'is_hr': employee.is_hr,
            'hr_scope': employee.hr_scope,
            'allow_site_checkin': employee.allow_site_checkin,
            'restrict_to_allowed_locations': employee.restrict_to_allowed_locations,
            'reminders': employee.reminders,
            'is_deleted': employee.is_deleted,
            'created_at': employee.created_at.isoformat() if employee.created_at else None,
            'updated_at': employee.updated_at.isoformat() if employee.updated_at else None,
            'company_name': company_name,
            'role_name': role_name,
            'department_name': department_name,
            'group_name': group_name,
            'reporting_manager_name': reporting_manager_name,
            'office_location_name': office_location_name,
            'work_policy_name': work_policy_name,
            'home_latitude': employee.home_latitude,
            'home_longitude': employee.home_longitude,
            'created_by': employee.created_by
        }
        
        return {
            'success': True,
            'employee': employee_data,
            'username': username,
            'message': 'Employee found successfully'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error retrieving employee: {str(e)}'
        }


if __name__ == "__main__":
    # Test the function
    test_username = input("Enter username to search: ")
    test_group_name = input("Enter group name (or press Enter to skip): ")
    test_company_name = input("Enter company name (or press Enter to skip): ")
    
    # Use provided names or None if empty
    group_name = test_group_name.strip() if test_group_name.strip() else None
    company_name = test_company_name.strip() if test_company_name.strip() else None
    
    result = user_by_username(test_username, company_name=company_name, group_name=group_name)
    print(result)