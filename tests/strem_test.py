from cdapython import Q
from tests.global_settings import host, table

q = Q('primary_disease_type = "Lung%"')
print(q.to_json())

q = q.run(host=host, table=table).to_dataframe()


print(q.head())
