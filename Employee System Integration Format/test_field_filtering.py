#!/usr/bin/env python3
"""
Test script to demonstrate field filtering functionality
"""

from Utils.confirmation_parser import parse_confirmation_response

# Mock employee details class for testing
class MockEmployeeDetails:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def filter_unchanged_fields(extracted_data, employee_details):
    """
    Filter out fields that are already the same as in the database
    (Copied from update_employee.py for testing)
    """
    if not employee_details:
        return extracted_data.model_dump(exclude_none=True)
    
    extracted_fields = extracted_data.model_dump(exclude_none=True)
    filtered_fields = {}
    
    # Field mapping from extracted data to database field names
    field_mapping = {
        'full_name': 'name',
        'first_name': 'first_name',
        'middle_name': 'middle_name', 
        'last_name': 'last_name',
        'emailId': 'email',
        'contact_number': 'contact_number',
        'company_name': 'company_name',
        'role': 'role',
        'work_policy_name': 'work_policy_name',
        'office_location_name': 'office_location_name',
        'department_name': 'department_name',
        'reporting_manager_name': 'reporting_manager_name',
        'designation': 'designation',
        'dateOfJoining': 'date_of_joining',
        'dateOfBirth': 'date_of_birth',
        'gender': 'gender',
        'home_latitude': 'home_latitude',
        'home_longitude': 'home_longitude',
        'allow_site_checkin': 'allow_site_checkin',
        'restrict_to_allowed_locations': 'restrict_to_allowed_locations',
        'reminders': 'reminders',
        'is_hr': 'is_hr',
        'hr_scope': 'hr_scope'
    }
    
    for field, value in extracted_fields.items():
        # Get the corresponding database field name
        db_field = field_mapping.get(field, field)
        
        # Get the current value from database
        current_value = getattr(employee_details, db_field, None)
        
        # Convert both values to strings for comparison (handle None values)
        current_str = str(current_value) if current_value is not None else ""
        new_str = str(value) if value is not None else ""
        
        # Only include field if values are different
        if current_str.lower().strip() != new_str.lower().strip():
            filtered_fields[field] = value
            print(f"  ✓ Field '{field}' changed: '{current_str}' → '{new_str}'")
        else:
            print(f"  ✗ Field '{field}' unchanged: '{current_str}' (skipping)")
    
    return filtered_fields

def test_field_filtering():
    """Test the field filtering functionality"""
    
    print("=" * 80)
    print("FIELD FILTERING TEST")
    print("=" * 80)
    
    # Mock extracted data (what user wants to update)
    class MockExtractedData:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
        
        def model_dump(self, exclude_none=True):
            result = {}
            for key, value in self.__dict__.items():
                if not exclude_none or value is not None:
                    result[key] = value
            return result
    
    # Test Case 1: Some fields changed, some unchanged
    print("\nTEST CASE 1: Mixed changes")
    print("-" * 40)
    
    # Current employee data in database
    current_employee = MockEmployeeDetails(
        name="John Doe",
        email="john.doe@company.com",
        contact_number="+971501234567",
        department="Engineering",
        designation="Senior Developer"
    )
    
    # What user wants to update
    extracted_data = MockExtractedData(
        emailId="john.doe@company.com",  # Same as current (should be filtered out)
        contact_number="+971509876543",  # Different (should be kept)
        department_name="Engineering",   # Same as current (should be filtered out)
        designation="Lead Developer"     # Different (should be kept)
    )
    
    print("Current employee data:")
    print(f"  Name: {current_employee.name}")
    print(f"  Email: {current_employee.email}")
    print(f"  Contact: {current_employee.contact_number}")
    print(f"  Department: {current_employee.department}")
    print(f"  Designation: {current_employee.designation}")
    
    print("\nUser wants to update:")
    print(f"  Email: {extracted_data.emailId}")
    print(f"  Contact: {extracted_data.contact_number}")
    print(f"  Department: {extracted_data.department_name}")
    print(f"  Designation: {extracted_data.designation}")
    
    print("\nFiltering results:")
    filtered_fields = filter_unchanged_fields(extracted_data, current_employee)
    
    print(f"\nFinal fields to update: {filtered_fields}")
    
    # Test Case 2: All fields unchanged
    print("\n\nTEST CASE 2: All fields unchanged")
    print("-" * 40)
    
    extracted_data2 = MockExtractedData(
        emailId="john.doe@company.com",  # Same as current
        contact_number="+971501234567",  # Same as current
        department_name="Engineering"    # Same as current
    )
    
    print("User wants to update (all same as current):")
    print(f"  Email: {extracted_data2.emailId}")
    print(f"  Contact: {extracted_data2.contact_number}")
    print(f"  Department: {extracted_data2.department_name}")
    
    print("\nFiltering results:")
    filtered_fields2 = filter_unchanged_fields(extracted_data2, current_employee)
    
    print(f"\nFinal fields to update: {filtered_fields2}")
    
    if not filtered_fields2:
        print("✅ No changes needed - all fields are already up to date!")
    
    # Test Case 3: All fields changed
    print("\n\nTEST CASE 3: All fields changed")
    print("-" * 40)
    
    extracted_data3 = MockExtractedData(
        emailId="john.smith@company.com",  # Different
        contact_number="+971509876543",    # Different
        department_name="Marketing"        # Different
    )
    
    print("User wants to update (all different):")
    print(f"  Email: {extracted_data3.emailId}")
    print(f"  Contact: {extracted_data3.contact_number}")
    print(f"  Department: {extracted_data3.department_name}")
    
    print("\nFiltering results:")
    filtered_fields3 = filter_unchanged_fields(extracted_data3, current_employee)
    
    print(f"\nFinal fields to update: {filtered_fields3}")

def show_benefits():
    """Show the benefits of field filtering"""
    
    print("\n" + "=" * 80)
    print("BENEFITS OF FIELD FILTERING")
    print("=" * 80)
    
    benefits = [
        "🎯 AVOIDS UNNECESSARY CONFIRMATIONS: No need to confirm fields that haven't changed",
        "⚡ FASTER USER EXPERIENCE: Users don't have to confirm obvious non-changes",
        "🧠 SMARTER SYSTEM: System understands what actually needs updating",
        "💬 CLEANER CONVERSATIONS: No confusing confirmations for unchanged data",
        "🔄 EFFICIENT UPDATES: Only processes fields that actually changed",
        "📊 BETTER LOGGING: Clear distinction between changed vs unchanged fields",
        "🛡️ PREVENTS ERRORS: Reduces chance of accidental overwrites",
        "✨ IMPROVED UX: Users see only relevant changes in confirmation"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")

if __name__ == "__main__":
    test_field_filtering()
    show_benefits()
