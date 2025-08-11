from update_employee import update_employee_fields
from proxies.proxy import EmployeeProxy
import pandas as pd
import os


exmployee_record = EmployeeProxy.get_employee_record(contact_number="+971501234567")

# We have put the default employee for testing as id 103 and the employee identfied as TRUE

# 35 test cases for role - varied natural messages with moderate typos
# 
test_cases = [
    ("please set role to Super Admin", 1),
    ("change role to Admin", 2),
    ("update role to HR Manager", 3),
    ("set the role as Team Lead", 4),
    ("make role Supervisor", 5),
    ("set role to Staff", 6),
    ("change role to Intern / Trainee", 7),
    ("update role to IT Admin / Tech Ops", 8),
    ("set role to Customer Support", 9),
    ("change role to Sales Executive", 10),
    ("set role as Engineer", 11),
    ("set role to General Manager", 15),
    ("please switch role to admin", 2),
    ("promote to Team Lead", 4),
    ("assign as Supervisor", 5),
    ("demote to Staff", 6),
    ("assign Intern/Trainee", 7),
    ("make them IT Admin Tech Ops", 8),
    ("put in Customer Support", 9),
    ("assign as Sales Exec", 10),
    ("set as Engineer", 11),
    ("update to GM", 15),
    ("role should be Super Admin", 1),
    ("change to HR manager", 3),
    ("set role: team-lead", 4),
    ("move role to supervisor", 5),
    ("set role to trainee", 7),
    ("update to Tech Ops", 8),
    ("switch to cust support", 9),
    ("set to sales executive", 10),
    ("make role engineer", 11),
    ("set to general manager", 15),
    # Moderate typos
    ("set role to Superadmin", 1),
    ("change role to HR manger", 3),
    ("set role to suprvisor", 5),
]
results = []
# Run role tests
for user_query, expected_id in test_cases:
    response = update_employee_fields(contact_number="+971501234567", user_message=user_query)
    #  NEVER CHANGE THIS PHONE NUMBER
    current_record = EmployeeProxy.get_employee_record(contact_number="+971598754234")
    role_id = getattr(current_record, "role_id", None)
    result = "PASS" if role_id == expected_id else "FAIL"
    results.append({"response": response, "query": user_query, "result": result})

print(results)

# Append results to existing Excel or create if missing
excel_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(excel_dir, "test_results.xlsx")
df = pd.DataFrame(results, columns=["response", "query", "result"])
df.columns = ["Response", "Query", "Result"]
if os.path.exists(excel_path):
    existing_df = pd.read_excel(excel_path)
    combined_df = pd.concat([existing_df, df], ignore_index=True)
    combined_df.to_excel(excel_path, index=False)
else:
    df.to_excel(excel_path, index=False)
        












