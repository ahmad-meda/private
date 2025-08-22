from proxies.employee_session_proxy import EmployeeSessionProxy
from Utils.agents import extract_data
from Utils.formats import EmployeeData
import json

def test_extraction_agent():
    """Test the extraction agent for hallucination issues"""
    
    print("=== EXTRACTION AGENT HALLUCINATION TEST ===\n")
    
    # Test cases that should NOT extract any data (potential hallucination scenarios)
    test_cases = [
        {
            "name": "Empty message",
            "messages": [
                {"role": "user", "content": ""}
            ],
            "expected_fields": []
        },
        {
            "name": "Only greetings",
            "messages": [
                {"role": "user", "content": "Hello, how are you?"}
            ],
            "expected_fields": []
        },
        {
            "name": "Vague response",
            "messages": [
                {"role": "user", "content": "I don't know"}
            ],
            "expected_fields": []
        },
        {
            "name": "Negative response",
            "messages": [
                {"role": "user", "content": "No, I don't have that information"}
            ],
            "expected_fields": []
        },
        {
            "name": "Partial name only",
            "messages": [
                {"role": "user", "content": "His name is John"}
            ],
            "expected_fields": ["full_name"]
        },
        {
            "name": "Only phone number",
            "messages": [
                {"role": "user", "content": "Phone number is +971501234567"}
            ],
            "expected_fields": ["contact_number"]
        },
        {
            "name": "Only email",
            "messages": [
                {"role": "user", "content": "Email is john@company.com"}
            ],
            "expected_fields": ["emailId"]
        },
        {
            "name": "Ambiguous name",
            "messages": [
                {"role": "user", "content": "The employee is called Smith"}
            ],
            "expected_fields": ["full_name"]
        },
        {
            "name": "Incomplete date",
            "messages": [
                {"role": "user", "content": "He joined in 2023"}
            ],
            "expected_fields": []
        },
        {
            "name": "Vague location",
            "messages": [
                {"role": "user", "content": "He works in Dubai"}
            ],
            "expected_fields": ["office_location_name"]
        },
        {
            "name": "Mixed valid and invalid data",
            "messages": [
                {"role": "user", "content": "Name is John Doe, phone is +971501234567, and he works somewhere in the city"}
            ],
            "expected_fields": ["full_name", "contact_number"]
        },
        {
            "name": "Conversation with context but no clear data",
            "messages": [
                {"role": "assistant", "content": "Please provide the employee's name and contact number."},
                {"role": "user", "content": "I'll get back to you with that information later"}
            ],
            "expected_fields": []
        },
        {
            "name": "Multiple messages with partial info",
            "messages": [
                {"role": "assistant", "content": "What's the employee's name?"},
                {"role": "user", "content": "John"},
                {"role": "assistant", "content": "What's the last name?"},
                {"role": "user", "content": "Doe"}
            ],
            "expected_fields": ["full_name"]
        },
        {
            "name": "Repeated information",
            "messages": [
                {"role": "user", "content": "His name is John Doe"},
                {"role": "assistant", "content": "Got it. What's his contact number?"},
                {"role": "user", "content": "I already told you his name is John Doe"}
            ],
            "expected_fields": ["full_name"]
        }
    ]
    
    hallucination_count = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"Input: {test_case['messages']}")
        
        try:
            # Extract data using the agent
            extracted_data = extract_data(test_case['messages'])
            
            # Get non-null fields
            extracted_fields = []
            for field_name, field_value in extracted_data.model_dump().items():
                if field_value is not None:
                    extracted_fields.append(field_name)
            
            print(f"Extracted fields: {extracted_fields}")
            print(f"Expected fields: {test_case['expected_fields']}")
            
            # Check for hallucination (extracting fields that shouldn't be extracted)
            hallucinated_fields = [field for field in extracted_fields if field not in test_case['expected_fields']]
            
            if hallucinated_fields:
                print(f"❌ HALLUCINATION DETECTED! Extracted unexpected fields: {hallucinated_fields}")
                hallucination_count += 1
            else:
                print("✅ No hallucination detected")
            
            # Check for missing expected fields
            missing_fields = [field for field in test_case['expected_fields'] if field not in extracted_fields]
            if missing_fields:
                print(f"⚠️  Missing expected fields: {missing_fields}")
            
            print(f"Extracted data: {json.dumps(extracted_data.model_dump(exclude_none=True), indent=2)}")
            print("-" * 80)
            
        except Exception as e:
            print(f"❌ Error in test: {str(e)}")
            print("-" * 80)
    
    print(f"\n=== TEST RESULTS ===")
    print(f"Total tests: {total_tests}")
    print(f"Hallucination cases: {hallucination_count}")
    print(f"Hallucination rate: {(hallucination_count/total_tests)*100:.1f}%")
    
    if hallucination_count > 0:
        print(f"\n❌ HALLUCINATION ISSUES FOUND! The extraction agent is making up data in {hallucination_count} out of {total_tests} test cases.")
        print("Recommendations:")
        print("1. Strengthen the system prompt to be more explicit about not hallucinating")
        print("2. Add validation rules to check extracted data against conversation context")
        print("3. Implement confidence scoring for extracted fields")
        print("4. Add more examples in the prompt showing what NOT to extract")
    else:
        print(f"\n✅ No hallucination issues detected! The extraction agent is working correctly.")

def test_with_real_conversations():
    """Test with some realistic conversation scenarios"""
    
    print("\n=== REALISTIC CONVERSATION TESTS ===\n")
    
    real_conversations = [
        {
            "name": "Typical employee creation flow",
            "messages": [
                {"role": "assistant", "content": "I'll help you add a new employee. What's their full name?"},
                {"role": "user", "content": "Ahmad Al Mansouri"},
                {"role": "assistant", "content": "Great! What's their contact number?"},
                {"role": "user", "content": "+971501234567"},
                {"role": "assistant", "content": "What's their email address?"},
                {"role": "user", "content": "ahmad.mansouri@company.com"},
                {"role": "assistant", "content": "What's their designation?"},
                {"role": "user", "content": "Software Engineer"}
            ],
            "expected_fields": ["full_name", "contact_number", "emailId", "designation"]
        },
        {
            "name": "User provides incomplete information",
            "messages": [
                {"role": "assistant", "content": "What's the employee's name?"},
                {"role": "user", "content": "I think it's Sarah something"},
                {"role": "assistant", "content": "Do you have their full name?"},
                {"role": "user", "content": "Let me check and get back to you"}
            ],
            "expected_fields": []
        },
        {
            "name": "User provides multiple pieces of info at once",
            "messages": [
                {"role": "assistant", "content": "Please provide the employee details."},
                {"role": "user", "content": "Name: Maria Garcia, Phone: +971502345678, Email: maria.garcia@company.com, Department: Marketing"}
            ],
            "expected_fields": ["full_name", "contact_number", "emailId", "department_name"]
        }
    ]
    
    for i, conv in enumerate(real_conversations, 1):
        print(f"Realistic Test {i}: {conv['name']}")
        
        try:
            extracted_data = extract_data(conv['messages'])
            extracted_fields = [field for field, value in extracted_data.model_dump().items() if value is not None]
            
            print(f"Extracted: {extracted_fields}")
            print(f"Expected: {conv['expected_fields']}")
            
            hallucinated = [f for f in extracted_fields if f not in conv['expected_fields']]
            if hallucinated:
                print(f"❌ HALLUCINATION: {hallucinated}")
            else:
                print("✅ No hallucination")
            
            print(f"Data: {json.dumps(extracted_data.model_dump(exclude_none=True), indent=2)}")
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("-" * 60)

if __name__ == "__main__":
    test_extraction_agent()
    test_with_real_conversations()