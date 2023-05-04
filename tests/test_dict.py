from cdapython import Q
from tests.global_settings import host

q1 = Q('primary_diagnosis_site = "Kidney"')
r1 = q1.run(offset=500, async_call=True, host=host)

print(r1)
