from services.employee_session_service import EmployeeSessionService

def save_skipped_fields_to_redis(contact_number: str, skipped_fields_list: list):
    """
    Save a list of skipped fields to Redis for a specific contact number.
    
    Args:
        contact_number (str): The contact number of the user
        skipped_fields_list (list): List of field names that were skipped
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        session_service = EmployeeSessionService()
        session_service.set_skipped_fields(contact_number, skipped_fields_list)
        print(f"Successfully stored skipped fields in Redis for {contact_number}: {skipped_fields_list}")
        return True
    except Exception as e:
        print(f"Error storing skipped fields in Redis: {e}")
        return False

def get_skipped_fields_from_redis(contact_number: str):
    """
    Retrieve skipped fields from Redis for a specific contact number.
    
    Args:
        contact_number (str): The contact number of the user
    
    Returns:
        list: List of skipped field names, empty list if none found
    """
    try:
        session_service = EmployeeSessionService()
        skipped_fields = session_service.get_skipped_fields(contact_number)
        print(f"Retrieved skipped fields from Redis for {contact_number}: {skipped_fields}")
        return skipped_fields
    except Exception as e:
        print(f"Error retrieving skipped fields from Redis: {e}")
        return []

def add_single_skipped_field(contact_number: str, field_name: str):
    """
    Add a single field to the skipped fields list in Redis.
    
    Args:
        contact_number (str): The contact number of the user
        field_name (str): The name of the field to add to skipped list
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        session_service = EmployeeSessionService()
        session_service.add_skipped_field(contact_number, field_name)
        print(f"Successfully added '{field_name}' to skipped fields for {contact_number}")
        return True
    except Exception as e:
        print(f"Error adding skipped field to Redis: {e}")
        return False

def clear_skipped_fields_for_contact(contact_number: str):
    """
    Clear all skipped fields for a specific contact number.
    
    Args:
        contact_number (str): The contact number of the user
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        session_service = EmployeeSessionService()
        session_service.clear_skipped_fields(contact_number)
        print(f"Successfully cleared skipped fields for {contact_number}")
        return True
    except Exception as e:
        print(f"Error clearing skipped fields from Redis: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # Example contact number
    contact = "+971501234567"
    
    # Example skipped fields
    skipped_fields = ["dateOfBirth", "middle_name", "home_latitude", "home_longitude"]
    
    # Save skipped fields to Redis
    save_skipped_fields_to_redis(contact, skipped_fields)
    
    # Retrieve skipped fields from Redis
    retrieved_fields = get_skipped_fields_from_redis(contact)
    
    # Add a single field
    add_single_skipped_field(contact, "gender")
    
    # Get updated list
    updated_fields = get_skipped_fields_from_redis(contact)
    
    # Clear all skipped fields
    clear_skipped_fields_for_contact(contact) 