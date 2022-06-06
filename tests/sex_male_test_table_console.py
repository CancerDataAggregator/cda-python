from cdapython import Q
from tests.global_settings import host

q1 = Q("sex = 'female'")
r = q1.subject.count.run(host=host)
print(r)
