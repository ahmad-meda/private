"""
Stopwords and patterns for confirmation parsing
"""

# Positive confirmation words/phrases
POSITIVE_CONFIRMATIONS = {
    'yes', 'yeah', 'yep', 'yup', 'sure', 'okay', 'ok', 'alright', 'fine',
    'go ahead', 'proceed', 'update', 'confirm', 'correct', 'right',
    'that\'s right', 'that is right', 'exactly', 'perfect', 'good',
    'sounds good', 'looks good', 'seems right', 'agreed', 'approve',
    'absolutely', 'definitely', 'certainly', 'of course', 'indeed',
    'true', 'accurate', 'valid', 'acceptable', 'satisfactory'
}

# Negative confirmation words/phrases
NEGATIVE_CONFIRMATIONS = {
    'no', 'nope', 'nah', 'not', 'don\'t', 'do not', 'cancel', 'stop',
    'nevermind', 'never mind', 'changed my mind', 'forget it',
    'not correct', 'not right', 'wrong', 'incorrect', 'mistake',
    'that\'s wrong', 'that is wrong', 'not what i meant',
    'disagree', 'reject', 'decline', 'refuse', 'deny',
    'false', 'inaccurate', 'invalid', 'unacceptable', 'unsatisfactory'
}

# Words indicating editing/modification
EDITING_INDICATORS = {
    'change', 'modify', 'edit', 'update', 'fix', 'correct', 'adjust',
    'instead', 'rather', 'actually', 'wait', 'hold on', 'but',
    'however', 'though', 'although', 'except', 'except for',
    'replace', 'switch', 'swap', 'alter', 'revise', 'amend',
    'make it', 'set it', 'put it', 'use', 'try', 'prefer'
}

# Words indicating wrong employee
WRONG_EMPLOYEE_INDICATORS = {
    'wrong employee', 'wrong person', 'not the right', 'not who i meant',
    'different employee', 'other employee', 'meant to update',
    'should be', 'supposed to be', 'that\'s not', 'that is not',
    'mistaken', 'confused', 'mixed up', 'wrong one', 'not him',
    'not her', 'not them', 'someone else', 'another person'
}

# Unrelated response indicators
UNRELATED_INDICATORS = {
    'what', 'how', 'when', 'where', 'why', 'who', 'help', 'confused',
    'don\'t know', 'do not know', 'not sure', 'maybe', 'think',
    'understand', 'explain', 'clarify', 'idk', 'i don\'t know',
    'question', 'ask', 'tell me', 'show me', 'guide me',
    'lost', 'stuck', 'problem', 'issue', 'error', 'trouble'
}

# Field names that can be updated
EMPLOYEE_FIELDS = {
    'name', 'full name', 'first name', 'last name', 'middle name',
    'email', 'email id', 'contact', 'phone', 'phone number', 'mobile',
    'company', 'company name', 'role', 'designation', 'position',
    'department', 'dept', 'manager', 'reporting manager', 'supervisor',
    'location', 'office location', 'work location', 'address',
    'policy', 'work policy', 'joining date', 'date of joining',
    'birth date', 'date of birth', 'dob', 'gender', 'sex',
    'latitude', 'longitude', 'coordinates', 'hr', 'is hr',
    'scope', 'hr scope', 'reminders', 'checkin', 'check-in',
    'site checkin', 'allowed locations', 'restricted locations'
}

# Farewell messages for different scenarios
FAREWELL_MESSAGES = {
    'decline': "No problem! The employee details remain unchanged. Let me know if you need help with anything else.",
    'cancel': "Update cancelled. The employee details remain unchanged. Feel free to reach out if you need any assistance.",
    'unclear': "I understand you're not sure. The employee details will remain unchanged. Please let me know if you'd like to make any updates later.",
    'unrelated': "I'm not sure I understand your response. The employee details will remain unchanged. Please let me know if you'd like to make any updates."
}

# Field name mapping to standard field names
FIELD_MAPPING = {
    'full name': 'full_name',
    'first name': 'first_name',
    'last name': 'last_name',
    'middle name': 'middle_name',
    'email': 'emailId',
    'email id': 'emailId',
    'contact': 'contact_number',
    'phone': 'contact_number',
    'phone number': 'contact_number',
    'mobile': 'contact_number',
    'company': 'company_name',
    'company name': 'company_name',
    'designation': 'designation',
    'position': 'designation',
    'department': 'department_name',
    'dept': 'department_name',
    'manager': 'reporting_manager_name',
    'reporting manager': 'reporting_manager_name',
    'supervisor': 'reporting_manager_name',
    'location': 'office_location_name',
    'office location': 'office_location_name',
    'work location': 'office_location_name',
    'policy': 'work_policy_name',
    'work policy': 'work_policy_name',
    'joining date': 'dateOfJoining',
    'date of joining': 'dateOfJoining',
    'birth date': 'dateOfBirth',
    'date of birth': 'dateOfBirth',
    'dob': 'dateOfBirth',
    'hr': 'is_hr',
    'is hr': 'is_hr',
    'scope': 'hr_scope',
    'hr scope': 'hr_scope',
    'checkin': 'allow_site_checkin',
    'check-in': 'allow_site_checkin',
    'site checkin': 'allow_site_checkin',
    'allowed locations': 'restrict_to_allowed_locations',
    'restricted locations': 'restrict_to_allowed_locations'
}

# Regex patterns for field:value extraction
FIELD_VALUE_PATTERNS = [
    r'(?:change|update|modify|set|make)\s+(\w+(?:\s+\w+)*)\s+to\s+([^.!?]+)',
    r'(\w+(?:\s+\w+)*)\s+should\s+be\s+([^.!?]+)',
    r'(\w+(?:\s+\w+)*)\s+is\s+([^.!?]+)',
    r'(\w+(?:\s+\w+)*)\s+=\s+([^.!?]+)',
    r'(\w+(?:\s+\w+)*):\s*([^.!?]+)',
    r'(?:also|and)\s+(?:change|update|modify|set|make)\s+(\w+(?:\s+\w+)*)\s+to\s+([^.!?]+)',
    r'(?:also|and)\s+(\w+(?:\s+\w+)*)\s+should\s+be\s+([^.!?]+)',
    r'(?:also|and)\s+(\w+(?:\s+\w+)*)\s+is\s+([^.!?]+)'
]
