from cdapython import Q
from tests.global_settings import host

r = Q('id = "TCGA-E2-A10A"').file.run(host=host)
print(r)
