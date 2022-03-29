from cdapython import Q
from tests.global_settings import host

q1 = Q('subject_associated_project = "TCGA-OV"')
r = q1.run(host=host)
print(r)
