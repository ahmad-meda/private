from Files.SQLAlchemyModels import Company, OfficeLocation, db
from proxies.proxy import EmployeeProxy

result = EmployeeProxy.get_companies_by_group_and_company(group_id=1, company_id=1)
print(result)