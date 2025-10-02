#!/usr/bin/env python3
"""
Demo script showing the complete confirmation system in action
"""

from Utils.confirmation_parser import parse_confirmation_response

def demo_confirmation_system():
    """Demonstrate the complete confirmation system"""
    
    print("=" * 80)
    print("EMPLOYEE UPDATE CONFIRMATION SYSTEM DEMO")
    print("=" * 80)
    print()
    
    # Simulate a confirmation message
    confirmation_message = """
    Are you sure you want to make the following changes to *John Doe*?
    
    • *email*: john.doe@company.com
    • *department*: Engineering
    """
    
    print("CONFIRMATION MESSAGE:")
    print(confirmation_message)
    print("-" * 50)
    
    # Test different user responses
    test_responses = [
        "yes, go ahead",
        "yes, but also change the phone number to +971501234567",
        "wait, change the email to john.smith@company.com instead",
        "that's not the right employee, I meant to update Sarah",
        "no, don't update",
        "idk, what to do.."
    ]
    
    for i, response in enumerate(test_responses, 1):
        print(f"\nTEST CASE {i}:")
        print(f"User Response: '{response}'")
        
        # Parse the response
        intent = parse_confirmation_response(response)
        
        # Display results
        print("Parsed Intent:")
        print(f"  ✓ Wants to update: {intent.does_user_want_to_update}")
        print(f"  ✏️  Mentioned editing: {intent.did_user_mention_editing}")
        print(f"  ❌ Wrong employee: {intent.is_wrong_employee}")
        print(f"  ❓ Unrelated response: {intent.is_unrelated_response}")
        
        if intent.additional_fields:
            print(f"  📝 Additional fields: {intent.additional_fields}")
        
        if intent.farewell_message:
            print(f"  💬 Farewell message: {intent.farewell_message}")
        
        # Simulate system response
        print("\nSystem Action:")
        if intent.does_user_want_to_update and not intent.did_user_mention_editing:
            print("  → Proceeding with update")
        elif intent.does_user_want_to_update and intent.did_user_mention_editing:
            print("  → Proceeding with update + additional changes")
        elif intent.did_user_mention_editing:
            print("  → Requesting clarification for edits")
        elif intent.is_wrong_employee:
            print("  → Resetting employee identification")
        elif intent.farewell_message:
            print("  → Ending conversation")
        else:
            print("  → Requesting clarification")
        
        print("-" * 50)

def show_benefits():
    """Show the benefits of using regex/stopwords over LLM"""
    
    print("\n" + "=" * 80)
    print("BENEFITS OF REGEX/STOPWORDS APPROACH")
    print("=" * 80)
    
    benefits = [
        "🚀 FASTER: No API calls to LLM - instant response",
        "💰 CHEAPER: No token costs for confirmation parsing",
        "🎯 MORE RELIABLE: Consistent pattern matching vs. LLM variability",
        "🔧 EASIER TO DEBUG: Clear patterns and rules",
        "📈 BETTER PERFORMANCE: No network latency",
        "🛡️ MORE SECURE: No external API dependencies",
        "🎛️ EASIER TO CUSTOMIZE: Add/modify patterns as needed",
        "📊 PREDICTABLE: Same input always gives same output"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")
    
    print("\n" + "=" * 80)
    print("PATTERN EXAMPLES")
    print("=" * 80)
    
    patterns = [
        ("Positive Confirmation", "yes, sure, okay, go ahead, that's correct"),
        ("Negative Confirmation", "no, don't, cancel, nevermind, wrong"),
        ("Editing Intent", "change, modify, instead, actually, but"),
        ("Wrong Employee", "wrong employee, not the right, meant to update"),
        ("Unrelated Response", "what, how, help, confused, don't know"),
        ("Field Extraction", "change email to john@company.com, phone should be +971...")
    ]
    
    for category, examples in patterns:
        print(f"\n{category}:")
        print(f"  Examples: {examples}")

if __name__ == "__main__":
    demo_confirmation_system()
    show_benefits()
