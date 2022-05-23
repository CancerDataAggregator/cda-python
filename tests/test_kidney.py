from cdapython import Q
from tests.global_settings import host, localhost

q1 = Q('ResearchSubject.primary_diagnosis_site = "Kidney"')
r1 = q1.run(limit=500, host=host)
print(r1)
