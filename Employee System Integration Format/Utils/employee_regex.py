import re

def extract_fields(message):
    """
    Simple function to extract employee fields from a message.
    Returns a dictionary with field names and their values + confidence scores.
    """
    
    # All the fields we want to extract
    fields = {
        "employee_id": None,
        "full_name": None, 
        "contact_number": None,
        "company_name": None,
        "role": None,
        "reporting_manager_name": None,
        "designation": None,
        "dateOfJoining": None,
        "dateOfBirth": None,
        "gender": None,
        "emailId": None,
        "department_name": None,
        "office_location_name": None,
        "reminders": None,
        "is_hr": None,
        "hr_scope": None
    }
    
    msg = message.lower()
    
    # Employee ID
    match = re.search(r"(?:employee\s*id|emp\s*id)\s*(?:is|:)?\s*([A-Za-z0-9\-_]+)", msg, re.I)
    if match: fields["employee_id"] = match.group(1)
    
    # Manager - check first (has priority over name for "under X" pattern)
    match = re.search(r"(?:under|reports?\s+to)\s+([A-Za-z\s\.]+?)(?:\s*$|\s+(?:and|with|,))", msg, re.I)
    if match: fields["reporting_manager_name"] = match.group(1).strip()
    
    if not fields["reporting_manager_name"]:
        match = re.search(r"(?:manager|supervisor)\s*(?:is|:)?\s*([A-Za-z\s\.]+?)(?:\s+(?:and|with|,)|\s*$)", msg, re.I)
        if match: fields["reporting_manager_name"] = match.group(1).strip()
    
    if not fields["reporting_manager_name"]:
        match = re.search(r"(?:her|his)\s+manager\s+is\s+([A-Za-z\s\.]+?)(?:\s+(?:and|with|,)|\s*$)", msg, re.I)
        if match: fields["reporting_manager_name"] = match.group(1).strip()
    
    # Full Name - check for "named X", "called X", "name is X", "info on X" (ONLY if not asking about manager)
    if "under" not in msg and "reports to" not in msg:
        match = re.search(r"named\s+([A-Za-z\s]+?)(?:\s+(?:and|with|,)|\s*$)", msg, re.I)
        if match: fields["full_name"] = match.group(1).strip()
        
        if not fields["full_name"]:
            match = re.search(r"called\s+([A-Za-z\s]+?)(?:\s+(?:and|with|,)|\s*$)", msg, re.I)
            if match: fields["full_name"] = match.group(1).strip()
        
        if not fields["full_name"]:
            match = re.search(r"name\s*(?:is|:)\s*([A-Za-z\s]+?)(?:\s+(?:and|with|,)|\s*$)", msg, re.I)
            if match: fields["full_name"] = match.group(1).strip()
        
        if not fields["full_name"]:
            match = re.search(r"info\s+(?:on|for)\s+([A-Za-z\s]+?)(?:\s*$|\s+(?:and|with|,))", msg, re.I)
            if match: fields["full_name"] = match.group(1).strip()
        
        if not fields["full_name"]:
            match = re.search(r"details\s+for\s+([A-Za-z\s]+?)(?:\s*$|\s+(?:and|with|,))", msg, re.I)
            if match: fields["full_name"] = match.group(1).strip()
    
    # Contact Number
    match = re.search(r"(?:contact\s*number|phone|mobile)\s*(?:is|:)?\s*([+\d\s\-\(\)]{10,20})", msg, re.I)
    if match: fields["contact_number"] = match.group(1).strip()
    
    if not fields["contact_number"]:
        match = re.search(r"(?:his|her)\s+phone\s+is\s+([+\d\s\-\(\)]{10,20})", msg, re.I)
        if match: fields["contact_number"] = match.group(1).strip()
    
    # Email
    match = re.search(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", message)
    if match: fields["emailId"] = match.group(1)
    
    # Company
    match = re.search(r"(?:company|organization)\s*(?:is|:)?\s*([A-Za-z\s\.&]+?)(?:\s+(?:and|with|,)|\s*$)", msg, re.I)
    if match: fields["company_name"] = match.group(1).strip()
    
    if not fields["company_name"]:
        match = re.search(r"works?\s+(?:at|for)\s+([A-Za-z\s\.&]+?)(?:\s+(?:and|with|,)|\s*$)", msg, re.I)
        if match: fields["company_name"] = match.group(1).strip()
    
    # Role
    match = re.search(r"(?:role|position)\s*(?:is|:)?\s*([A-Za-z\s]+?)(?:\s+(?:and|with|at|,)|\s*$)", msg, re.I)
    if match: fields["role"] = match.group(1).strip()
    
    if not fields["role"]:
        match = re.search(r"works?\s+as\s+([A-Za-z\s]+?)(?:\s+(?:and|with|at|,)|\s*$)", msg, re.I)
        if match: fields["role"] = match.group(1).strip()
    
    # Department
    match = re.search(r"(?:department|dept)\s*(?:is|:)?\s*([A-Za-z\s]+?)(?:\s+(?:and|with|,)|\s*$)", msg, re.I)
    if match: fields["department_name"] = match.group(1).strip()
    
    # Designation
    match = re.search(r"designation\s*(?:is|:)?\s*([A-Za-z\s]+?)(?:\s+(?:and|with|,)|\s*$)", msg, re.I)
    if match: fields["designation"] = match.group(1).strip()
    
    # Office Location
    match = re.search(r"(?:location|office|branch)\s*(?:is|:)?\s*([A-Za-z\s,]+?)(?:\s+(?:and|with)|\s*$)", msg, re.I)
    if match: fields["office_location_name"] = match.group(1).strip()
    
    # Date of Joining
    match = re.search(r"(?:joining\s*date|start\s*date|doj|joined)\s*(?:is|:)?\s*([0-9]{1,2}[\/\-][0-9]{1,2}[\/\-][0-9]{2,4})", msg, re.I)
    if match: fields["dateOfJoining"] = match.group(1)
    
    # Date of Birth
    match = re.search(r"(?:birth\s*date|dob|born)\s*(?:is|:)?\s*([0-9]{1,2}[\/\-][0-9]{1,2}[\/\-][0-9]{2,4})", msg, re.I)
    if match: fields["dateOfBirth"] = match.group(1)
    
    # Gender
    match = re.search(r"(?:gender|sex)\s*(?:is|:)?\s*(male|female|other|m|f)", msg, re.I)
    if match: fields["gender"] = match.group(1)
    
    # Reminders
    match = re.search(r"(?:reminders?|notifications?)\s*(?:is|are)?\s*(yes|no|true|false|on|off)", msg, re.I)
    if match: fields["reminders"] = match.group(1)
    
    # HR
    match = re.search(r"hr\s*(?:is|:)?\s*(yes|no|true|false)", msg, re.I)
    if match: fields["is_hr"] = match.group(1)
    
    # HR Scope
    match = re.search(r"(?:hr\s*scope|scope)\s*(?:is|:)?\s*(company|department|team|global)", msg, re.I)
    if match: fields["hr_scope"] = match.group(1)
    
    # Create result with confidence scores
    result = {}
    for field_name, value in fields.items():
        if value:
            result[field_name] = {"value": value, "confidence": 85}
        else:
            result[field_name] = {"value": None, "confidence": 100}
    
    return result

# Test it
if __name__ == "__main__":
    test_message = "pls give me info on the employee with the contact number +971561101062"
    result = extract_fields(test_message)
    
    print("Extracted fields:")
    for field, data in result.items():
        if data["value"]:
            print(f"{field}: {data['value']} (confidence: {data['confidence']}%)")
        else:
            print(f"{field}: None (confidence: {data['confidence']}%)")