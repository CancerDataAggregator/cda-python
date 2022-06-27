from cdapython import Q
from tests.global_settings import host

q = Q('id = "TCGA-13-1409"')  # note the double quotes for the string value
r = q.subject.file.run(host=host)
print(r)
