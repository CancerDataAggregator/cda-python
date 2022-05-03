from tests.global_settings import host, localhost
from cdapython import Q

q1 = Q('ResearchSubject.primary_diagnosis_site = "Kidney"')
r1 = q1.run(limit=500, host=localhost)
print(r1)
