from typing import List, Dict, Optional
from proxies.proxy import EmployeeProxy


def get_employee_details_by_role(role_name: str, company_name: str = None, group_name: str = None) -> Dict:
    """
    Get employee details by role with company/group filtering
    
    Args:
        role_name: The role name to search for
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
        # Validation: Check if role_name is provided
        if not role_name or not role_name.strip():
            return {
                'success': False,
                'error': 'Role name is required'
            }
        
        # Strip whitespace
        role_name = role_name.strip()
        
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
        
        # Use the efficient filtering method
        employees, error = EmployeeProxy.get_employees_by_role_employee_list(role_name, company_id=company_id, group_id=group_id)
        print(employees)
        print(error)
        if error:
            return {
                'success': False,
                'error': error.get('error', 'Unknown error occurred')
            }
        
        # Create list of dictionaries with only ID and username
        employee_list = []
        for emp in employees:
            employee_data = {
                'id': emp.id,
                'username': emp.username if emp.username else None
            }
            employee_list.append(employee_data)
        
        # Return the employee list with ID and username only
        return {
            'success': True,
            'employees': employee_list,
            'role_name': role_name,
            'total_count': len(employee_list),
            'message': 'Employee data retrieved successfully'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error occurred: {str(e)}'
        }


# result = get_employee_details_by_role("Staff", company_name="Acme Corporation")
# print(result)
