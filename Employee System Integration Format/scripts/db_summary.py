from collections import defaultdict
import sys, os

# Ensure project root is on path when running from scripts/
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app
from database import db
from Files.SQLAlchemyModels import Company, Employee, Group


def main() -> None:
    with app.app_context():
        total_companies = db.session.query(Company).count()
        total_groups = db.session.query(Group).count()
        total_employees = db.session.query(Employee).count()

        # Employees per company
        company_rows = db.session.query(Company).all()
        company_employee_counts = {}
        for c in company_rows:
            count = db.session.query(Employee).filter(Employee.company_id == c.id, Employee.is_deleted == False).count()
            company_employee_counts[c.id] = {
                "id": c.id,
                "name": c.name,
                "group_id": c.group_id,
                "employee_count": count,
            }

        # Group → companies
        groups = db.session.query(Group).all()
        group_summary = []
        for g in groups:
            # Companies in this group
            companies_in_group = [v for v in company_employee_counts.values() if v["group_id"] == g.id]
            company_count = len(companies_in_group)
            # Employees in this group (via Employee.group_id)
            employees_in_group = db.session.query(Employee).filter(Employee.group_id == g.id, Employee.is_deleted == False).count()
            group_summary.append({
                "id": g.id,
                "name": g.name,
                "company_count": company_count,
                "employee_count": employees_in_group,
                "companies": sorted(
                    [
                        {
                            "id": c["id"],
                            "name": c["name"],
                            "employee_count": c["employee_count"],
                        }
                        for c in companies_in_group
                    ],
                    key=lambda x: x["name"].lower(),
                ),
            })

        # Ungrouped companies (group_id is None)
        ungrouped_companies = [v for v in company_employee_counts.values() if v["group_id"] is None]
        # Employees with no group (Employee.group_id is None)
        ungrouped_employee_count = db.session.query(Employee).filter(Employee.group_id.is_(None), Employee.is_deleted == False).count()

        # Print summary
        print("=== Totals ===")
        print(f"Companies: {total_companies}")
        print(f"Groups:    {total_groups}")
        print(f"Employees: {total_employees}")

        print("\n=== Groups ===")
        for g in group_summary:
            print(f"Group {g['id']}: {g['name']}  | companies={g['company_count']}  employees={g['employee_count']}")
            for c in g["companies"]:
                print(f"  - {c['name']} (id={c['id']}): employees={c['employee_count']}")

        print("\n=== Ungrouped Companies ===")
        if not ungrouped_companies:
            print("(none)")
        else:
            for c in sorted(ungrouped_companies, key=lambda x: x["name"].lower()):
                print(f"- {c['name']} (id={c['id']}): employees={c['employee_count']}")

        print("\nEmployees without group:", ungrouped_employee_count)


if __name__ == "__main__":
    main()

