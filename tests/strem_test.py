from cdapython import Q
from tests.global_settings import dev_host, table_dev

q = Q('primary_disease_type = "Lung%"')
print(q.to_json())

q = q.to_dataframe()


print(q.head())
