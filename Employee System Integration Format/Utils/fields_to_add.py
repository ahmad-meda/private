class AgentStates:
    def __init__(self):
        self.mandatory_fields = [
            "full_name", "contact_number", "company_name","role", "reporting_manager_name","designation", "dateOfJoining", "dateOfBirth", "gender", "emailId"
        ]
        self.optional_personal_fields = [
            # "emailId", "dateOfBirth", "gender"
            "reminders", "is_hr", "hr_scope"
        ]
        self.optional_employment_fields = [
            "department_name", "office_location_name",
            # "designation", "dateOfJoining", "role", "reporting_manager_name", "department_name", "work_policy_name"
        ]
        self.optional_location_fields = [
            # "office_location_name"
        ]
        
agent_states = AgentStates()

