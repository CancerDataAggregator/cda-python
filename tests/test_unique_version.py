from cdapython import unique_terms
from tests.global_settings import host

print(unique_terms("vital_status", version="all_v2_1", host=host))
