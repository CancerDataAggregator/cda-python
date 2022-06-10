from cdapython import Q
from tests.global_settings import host

q1 = Q('ResearchSubject.Diagnosis.stage = "Stage I"')
q2 = Q('ResearchSubject.Diagnosis.stage = "Stage II"')
q3 = Q("ResearchSubject.primary_diagnosis_site = 'Kidney'")
q_diag = q1.OR(q2)
q = q_diag.AND(q3)
# print(q.counts.run())
qsub = q.subject.count.run(show_sql=True, host=host)
print(qsub)
