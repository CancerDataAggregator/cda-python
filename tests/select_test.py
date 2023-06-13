from cdapython import Q
from tests.global_settings import host, project

a = Q("sex = 'male' AND NOT vital_status = 'Dead'  ").SELECT("vital_status,sex")
print(a.to_json())
print(a.run(host=host, table=project))
