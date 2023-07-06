from cdapython import Q
from tests.global_settings import localhost

q1 = Q('system = "PDC"')
q2 = Q('system = "GDC"')
q3 = Q('system = "IDC"')

Q('system = "PDC" FROM system = "GDC" FROM system = "IDC"')


q = q3.FROM(q1.FROM(q2))

r = q.run(host=localhost, limit=100)

print(r)

tmp = {}
for i in r.paginator():
    tmp = {**i.to_dict()}
    print(i)

print(len(tmp))
