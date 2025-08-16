from proxies.proxy import EmployeeProxy
from Utils.fields_to_add import agent_states

def get_null_fields(draft_id):
    null_fields = EmployeeProxy.get_null_fields(draft_id)
    if null_fields:
        main_fields = [field for field in agent_states.mandatory_fields if field in null_fields]
        optional_personal_fields = [field for field in agent_states.optional_personal_fields if field in null_fields]
        optional_employment_fields = [field for field in agent_states.optional_employment_fields if field in null_fields]
        optional_location_fields = [field for field in agent_states.optional_location_fields if field in null_fields]

    return main_fields, optional_personal_fields, optional_employment_fields, optional_location_fields