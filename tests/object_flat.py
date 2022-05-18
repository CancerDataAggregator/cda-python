from copy import copy

from numpy import sort
from pandas import DataFrame

from cdapython import Q, Result
from tests.global_settings import localhost

q1 = Q('ResearchSubject.identifier.system = "PDC"')
q2 = Q('ResearchSubject.identifier.system = "GDC"')
q3 = Q('identifier.system = "IDC"')

q = q3.From(q1.From(q2))

r = q.run(host=localhost, limit=100)

print(r)

tmp = {}
for i in r.paginator():
    tmp = {**i.to_dict()}
    print(i)

print(len(tmp))
