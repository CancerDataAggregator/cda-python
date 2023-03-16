from cdapython import Q
from tests.global_settings import host

q1 = Q('ResearchSubject.identifier.system = "PDC"')
q2 = Q('ResearchSubject.identifier.system = "GDC"')
q3 = Q('identifier.system = "IDC"')

q = q3.FROM(q1.FROM(q2))
r = q.run(host=host, limit=1000)

r.to_dataframe().to_csv("data.csv")
