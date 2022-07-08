from cdapython import unique_terms
from tests.global_settings import host, table

print(unique_terms("vital_status", host=host, table=table))
