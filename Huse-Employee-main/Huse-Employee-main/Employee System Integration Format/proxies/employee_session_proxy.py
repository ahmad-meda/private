from services.employee_session_service import EmployeeSessionService

class EmployeeSessionProxy:
    # Create one instance to use everywhere
    _service = EmployeeSessionService()
    
    @classmethod
    def set_employee_identified(cls, contact_number, is_identified):
        """Store if employee is identified"""
        return cls._service.set_employee_identified(contact_number, is_identified)
    
    @classmethod
    def get_employee_identified(cls, contact_number):
        """Get if employee is identified (returns False if not found)"""
        return cls._service.get_employee_identified(contact_number)
    
    @classmethod
    def set_employee_id(cls, contact_number, employee_id):
        """Store employee ID"""
        return cls._service.set_employee_id(contact_number, employee_id)
    
    @classmethod
    def get_employee_id(cls, contact_number):
        """Get employee ID (returns None if not found)"""
        return cls._service.get_employee_id(contact_number)
    
    @classmethod
    def clear_employee_session(cls, contact_number):
        """Clear all employee data for this contact"""
        return cls._service.clear_employee_session(contact_number)

    @classmethod
    def add_to_list(cls, contact_number, items):
        """Add items to list"""
        return cls._service.add_to_list(contact_number, items)
    
    @classmethod
    def clear_list(cls, contact_number):
        """Clear the list"""
        return cls._service.clear_list(contact_number)

    @classmethod
    def get_list(cls, contact_number):
        """Get the list"""
        return cls._service.get_list(contact_number)
    
    @classmethod
    def clear_messages(cls, contact_number):
        """Clear all messages for a given contact number"""
        return cls._service.clear_messages(contact_number)
    
    @classmethod
    def add_message(cls, contact_number, message):
        """Add a message to the contact's history"""
        return cls._service.add_message(contact_number, message)    

    @classmethod
    def get_messages(cls, contact_number):
        """Get all messages for a given contact number"""
        return cls._service.get_messages(contact_number)