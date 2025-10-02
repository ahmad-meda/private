#!/usr/bin/env python3
"""
Example usage of the confirmation parser in a real scenario
"""

from Utils.confirmation_parser import parse_confirmation_response

def handle_confirmation_response(user_message: str, employee_name: str, fields_to_update: dict):
    """
    Example function showing how to handle confirmation responses
    """
    print(f"Employee: {employee_name}")
    print(f"Fields to update: {fields_to_update}")
    print(f"User response: '{user_message}'")
    print("-" * 50)
    
    # Parse the user's response
    intent = parse_confirmation_response(user_message)
    
    if intent.does_user_want_to_update and not intent.did_user_mention_editing:
        # User confirmed all changes
        print("✅ User confirmed all changes - proceeding with update")
        return "update_confirmed", fields_to_update
        
    elif intent.does_user_want_to_update and intent.did_user_mention_editing:
        # User confirmed but wants to add/modify fields
        print("✅ User confirmed with additional changes")
        print(f"Additional fields: {intent.additional_fields}")
        
        # Merge additional fields
        updated_fields = {**fields_to_update, **intent.additional_fields}
        return "update_confirmed_with_changes", updated_fields
        
    elif intent.did_user_mention_editing and not intent.does_user_want_to_update:
        # User wants to edit before confirming
        print("✏️ User wants to edit details before confirming")
        print(f"Additional fields: {intent.additional_fields}")
        return "edit_requested", intent.additional_fields
        
    elif intent.is_wrong_employee:
        # User indicated wrong employee
        print("❌ User indicated wrong employee")
        return "wrong_employee", None
        
    elif intent.farewell_message:
        # User declined or gave unclear response
        print(f"❌ User declined or unclear: {intent.farewell_message}")
        return "declined", None
        
    else:
        # Default case
        print("❓ Unclear response")
        return "unclear", None

def main():
    """Demonstrate the confirmation parser in action"""
    
    # Example 1: User confirms all changes
    print("EXAMPLE 1: User confirms all changes")
    result = handle_confirmation_response(
        "yes, go ahead",
        "John Doe",
        {"email": "john.doe@company.com", "department": "Engineering"}
    )
    print(f"Result: {result}\n")
    
    # Example 2: User confirms but adds more fields
    print("EXAMPLE 2: User confirms but adds more fields")
    result = handle_confirmation_response(
        "yes, but also change the phone number to +971501234567",
        "John Doe",
        {"email": "john.doe@company.com", "department": "Engineering"}
    )
    print(f"Result: {result}\n")
    
    # Example 3: User wants to edit
    print("EXAMPLE 3: User wants to edit")
    result = handle_confirmation_response(
        "wait, change the email to john.smith@company.com instead",
        "John Doe",
        {"email": "john.doe@company.com", "department": "Engineering"}
    )
    print(f"Result: {result}\n")
    
    # Example 4: User says wrong employee
    print("EXAMPLE 4: User says wrong employee")
    result = handle_confirmation_response(
        "that's not the right employee, I meant to update Sarah",
        "John Doe",
        {"email": "john.doe@company.com", "department": "Engineering"}
    )
    print(f"Result: {result}\n")
    
    # Example 5: User declines
    print("EXAMPLE 5: User declines")
    result = handle_confirmation_response(
        "no, don't update",
        "John Doe",
        {"email": "john.doe@company.com", "department": "Engineering"}
    )
    print(f"Result: {result}\n")
    
    # Example 6: Unrelated response
    print("EXAMPLE 6: Unrelated response")
    result = handle_confirmation_response(
        "idk, what to do..",
        "John Doe",
        {"email": "john.doe@company.com", "department": "Engineering"}
    )
    print(f"Result: {result}\n")

if __name__ == "__main__":
    main()
