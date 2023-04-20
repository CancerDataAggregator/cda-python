from cdapython import unique_terms
from tests.global_settings import host, project

print(unique_terms("vital_status", host=host, table=project))
