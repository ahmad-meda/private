def separate_name(full_name):
    name_parts = full_name.split() if full_name else []
    first_name = name_parts[0] if name_parts else None
    middle_name = ' '.join(name_parts[1:-1]) if len(name_parts) > 2 else None
    last_name = name_parts[-1] if len(name_parts) > 1 else None
    return first_name, middle_name, last_name


def format_employee_list(employees):
    """
    Format a list of employee dictionaries into a WhatsApp-friendly message format.
    
    Args:
        employees (list): List of employee dictionaries
        
    Returns:
        str: Formatted WhatsApp message string of all employees
    """
    if not employees:
        return "📭 *No employees to display* 😔"
    
    message_parts = []
    message_parts.append("👥 *EMPLOYEE DIRECTORY* 👥")
    message_parts.append(f"📊 *Total Employees:* {len(employees)}")
    message_parts.append("━━━━━━━━━━━━━━━━━━━━━")
    
    for i, emp in enumerate(employees, 1):
        # Extract key information with fallbacks for None values
        emp_id = emp.get('employeeId', 'N/A')
        first_name = emp.get('first_name', 'N/A')
        middle_name = emp.get('middle_name', 'N/A')
        last_name = emp.get('last_name', 'N/A')
        name = emp.get('name', 'N/A')
        email = emp.get('emailId', 'N/A')
        designation = emp.get('designation', 'N/A')
        join_date = emp.get('dateOfJoining', 'N/A')
        birth_date = emp.get('dateOfBirth', 'N/A')
        contact = emp.get('contactNo', 'N/A')
        gender = emp.get('gender', 'N/A')
        office_location_id = emp.get('office_location_id', 'N/A')
        work_policy_id = emp.get('work_policy_id', 'N/A')
        home_latitude = emp.get('home_latitude', 'N/A')
        home_longitude = emp.get('home_longitude', 'N/A')
        company_id = emp.get('company_id', 'N/A')
        group_id = emp.get('group_id', 'N/A')
        reporting_manager_id = emp.get('reporting_manager_id', 'N/A')
        role_id = emp.get('role_id', 'N/A')
        department_id = emp.get('department_id', 'N/A')
        
        # Format gender emoji
        gender_emoji = "👨" if gender.lower() in ['male', 'm'] else "👩" if gender.lower() in ['female', 'f'] else "👤"
        
        # Format the employee block for WhatsApp
        message_parts.append(f"\n{gender_emoji} *Employee #{i}*")
        message_parts.append(f"🆔 *ID:* {emp_id}")
        message_parts.append(f"📝 *Name:* {name}")
        if first_name != 'N/A' or middle_name != 'N/A' or last_name != 'N/A':
            name_parts = f"{first_name}"
            if middle_name != 'N/A':
                name_parts += f" {middle_name}"
            if last_name != 'N/A':
                name_parts += f" {last_name}"
            message_parts.append(f"   ├ _Parts:_ {name_parts}")
        
        message_parts.append(f"💼 *Position:* {designation}")
        message_parts.append(f"📧 *Email:* {email}")
        message_parts.append(f"📱 *Contact:* {contact}")
        message_parts.append(f"🎂 *Birth Date:* {birth_date}")
        message_parts.append(f"📅 *Joined:* {join_date}")
        
        # Company & Organization Info
        message_parts.append(f"🏢 *Company ID:* {company_id}")
        message_parts.append(f"👥 *Group ID:* {group_id}")
        message_parts.append(f"🎭 *Role ID:* {role_id}")
        message_parts.append(f"🏬 *Department ID:* {department_id}")
        
        # Management & Location
        if reporting_manager_id != 'N/A':
            message_parts.append(f"👨‍💼 *Manager ID:* {reporting_manager_id}")
        message_parts.append(f"📍 *Office Location ID:* {office_location_id}")
        message_parts.append(f"📋 *Work Policy ID:* {work_policy_id}")
        
        # Home coordinates if available
        if home_latitude != 'N/A' and home_longitude != 'N/A':
            message_parts.append(f"🏠 *Home:* {home_latitude}, {home_longitude}")
        
        # Separator between employees
        if i < len(employees):
            message_parts.append("┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈")
    
    return "\n".join(message_parts)