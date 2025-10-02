#!/usr/bin/env python3
"""
Test script for the confirmation parser to demonstrate different scenarios
"""

from Utils.confirmation_parser import parse_confirmation_response

def test_confirmation_scenarios():
    """Test various confirmation scenarios"""
    
    test_cases = [
        # Scenario 1: User agrees with all changes
        ("yes, go ahead", "Positive confirmation"),
        ("sure, update it", "Positive confirmation"),
        ("okay", "Positive confirmation"),
        ("that's correct", "Positive confirmation"),
        
        # Scenario 2: User wants to edit/modify details
        ("wait, change the email to john.doe@company.com", "Editing intent"),
        ("actually, make the designation Senior Manager instead", "Editing intent"),
        ("no, update the phone number to +971501234567", "Editing intent"),
        ("can you change the department to Engineering?", "Editing intent"),
        
        # Scenario 3: User says wrong employee
        ("that's not the right employee", "Wrong employee"),
        ("I meant to update Ahmad, not Ali", "Wrong employee"),
        ("wrong person, I want to update Sarah", "Wrong employee"),
        ("that's not who I meant", "Wrong employee"),
        
        # Scenario 4: User declines/doesn't want to update
        ("no, don't update", "Negative confirmation"),
        ("cancel", "Negative confirmation"),
        ("nevermind", "Negative confirmation"),
        ("I changed my mind", "Negative confirmation"),
        
        # Scenario 5: Vague/Unclear responses
        ("maybe", "Unclear response"),
        ("I don't know", "Unclear response"),
        ("not sure", "Unclear response"),
        ("let me think about it", "Unclear response"),
        
        # Scenario 6: Partial agreement with additional changes
        ("yes, but also change the department to HR", "Positive with additional fields"),
        ("sure, and update the phone number too", "Positive with additional fields"),
        ("okay, but make the email john.smith@company.com", "Positive with additional fields"),
        
        # Scenario 7: Unrelated responses
        ("what will happen if I update this?", "Unrelated response"),
        ("idk, what to do..", "Unrelated response"),
        ("help me understand", "Unrelated response"),
        ("I'm confused", "Unrelated response"),
    ]
    
    print("=" * 80)
    print("CONFIRMATION PARSER TEST RESULTS")
    print("=" * 80)
    
    for user_input, expected_scenario in test_cases:
        result = parse_confirmation_response(user_input)
        
        print(f"\nInput: '{user_input}'")
        print(f"Expected: {expected_scenario}")
        print(f"Parsed Intent:")
        print(f"  - Wants to update: {result.does_user_want_to_update}")
        print(f"  - Mentioned editing: {result.did_user_mention_editing}")
        print(f"  - Wrong employee: {result.is_wrong_employee}")
        print(f"  - Unrelated response: {result.is_unrelated_response}")
        print(f"  - Farewell message: {result.farewell_message[:50] + '...' if len(result.farewell_message) > 50 else result.farewell_message}")
        print(f"  - Additional fields: {result.additional_fields}")
        print("-" * 40)

if __name__ == "__main__":
    test_confirmation_scenarios()
