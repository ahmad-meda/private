def safe_attr(obj, *attrs, default="N/A"):
    for attr in attrs:
        if obj is None:
            return default
        obj = getattr(obj, attr, None)
    return obj if obj is not None else default

def clean_employee_fields(extraction_result):
    """
    Clean the extraction result and return simple field-value pairs for database queries
    Handles both extraction patterns:
    1. Separate field objects: [{"field_name": "emailId", "field_value": "email"}, {"field_name": "employeeId", "field_value": "EMP123"}]
    2. Combined field objects: [{"field_name": "emailId", "field_value": "email", "fields": [{"employeeId": "EMP123"}]}]
    
    Args:
        extraction_result: The result from extract_employee_search_data()
    
    Returns:
        List of tuples: [("name", "Ahmad"), ("emailId", "email"), ("employeeId", "EMP123")]
    """
    cleaned_fields = []
    seen_fields = set()  # Track seen field-value pairs to avoid duplicates
    
    for field_obj in extraction_result.fields:
        # Add the main field if not already seen
        main_field = (field_obj.field_name, field_obj.field_value)
        if main_field not in seen_fields:
            cleaned_fields.append(main_field)
            seen_fields.add(main_field)
        
        # Check if there are additional fields in the nested fields array
        if hasattr(field_obj, 'fields') and field_obj.fields:
            for nested_field in field_obj.fields:
                # Extract all non-None fields from the nested field object
                for attr_name in ['employeeId', 'name', 'emailId', 'designation', 'dateOfJoining', 
                                'dateOfBirth', 'contactNo', 'gender', 'office_location_name', 
                                'work_policy_name', 'home_latitude', 'home_longitude', 
                                'company_name', 'group_name', 'reporting_manager_name', 
                                'role_name', 'department_name', 'checked_in', 'checked_out']:
                    attr_value = getattr(nested_field, attr_name, None)
                    if attr_value is not None:
                        nested_field_pair = (attr_name, attr_value)
                        if nested_field_pair not in seen_fields:
                            cleaned_fields.append(nested_field_pair)
                            seen_fields.add(nested_field_pair)
    
    return cleaned_fields

# Usage example:
# extraction_result = extract_employee_search_data(messages)
# clean_data = clean_employee_fields(extraction_result)
# print(clean_data)
# Output: [("name", "Sudheer"), ("name", "Ahmad")]

def format_employee_details(employee):
    """Format employee details in a neat way - returns a list containing a single string"""
    if not employee:
        return ["No employee found"]

    return [', '.join([
        f"Employee ID: {safe_attr(employee, 'employeeId')}",
        f"Full Name: {safe_attr(employee, 'name')}",
        f"First Name: {safe_attr(employee, 'first_name')}",
        f"Middle Name: {safe_attr(employee, 'middle_name')}",
        f"Last Name: {safe_attr(employee, 'last_name')}",
        f"Email ID: {safe_attr(employee, 'emailId')}",
        f"Designation: {safe_attr(employee, 'designation')}",
        f"Department: {safe_attr(employee, 'department', 'name')}",
        f"Role: {safe_attr(employee, 'role', 'name')}",
        f"Company: {safe_attr(employee, 'company', 'name')}",
        f"Group: {safe_attr(employee, 'group', 'name')}",
        f"Date of Joining: {safe_attr(employee, 'dateOfJoining')}",
        f"Date of Birth: {safe_attr(employee, 'dateOfBirth')}",
        f"Office Location: {safe_attr(employee, 'office_location', 'name')}",
        f"Work Policy: {safe_attr(employee, 'work_policy', 'name')}",
        f"Home Latitude: {safe_attr(employee, 'home_latitude')}",
        f"Home Longitude: {safe_attr(employee, 'home_longitude')}",
        f"Contact Number: {safe_attr(employee, 'contactNo')}",
        f"Gender: {safe_attr(employee, 'gender')}",
        f"Reporting Manager: {safe_attr(employee, 'reporting_manager', 'name')}",
    ])]