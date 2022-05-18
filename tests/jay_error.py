from cdapython import Q
from tests.global_settings import host, localhost

q1 = Q('ResearchSubject.identifier.system = "PDC"')
q2 = Q('ResearchSubject.identifier.system = "GDC"')
q3 = Q('identifier.system = "IDC"')

q = q3.From(q1.From(q2))
r = q.run(host=localhost, limit=1000)

r.to_dataframe().to_csv("data.csv")
