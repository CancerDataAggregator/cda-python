from cdapython import Q
from tests.global_settings import host, table

q1 = Q("ResearchSubject.Diagnosis.age_at_diagnosis > 50*365")
q2 = Q('ResearchSubject.associated_project = "TCGA-OV"')
q = q1.AND(q2)

r = q.run(host=host, table=table)
print(r.to_dataframe().head())
