from cdapython import Q
from tests.global_settings import host

q = Q('Subject.id = "TCGA-13-1409"')  # note the double quotes for the string value
r = q.files(host=host)
print(r)
