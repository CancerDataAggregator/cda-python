from pandas import DataFrame
from cdapython import Q
from pandas import DataFrame
from tests.global_settings import host

q1 = Q("ResearchSubject.Diagnosis.age_at_diagnosis > 50*365")
q2 = Q('ResearchSubject.associated_project = "TCGA-OV"')
q = q1.And(q2)
r = q.run(host=host)
# t = r.stream()

# if isinstance(t, DataFrame):
#     print(t.to_DataFrame())
