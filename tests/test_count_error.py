from cdapython import Q
from tests.global_settings import host

q1 = Q('primary_disease_type = "Nevi and Melanomas"')

q = q1
print(q)
r = q.count.run(host=host)

print(r)
