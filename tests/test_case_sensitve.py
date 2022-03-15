from cdapython import Q
from tests.global_settings import host
q = Q('id = "tcga-13-1409"')  # note the double quotes for the string value
r3_1 = q.run(
    host=host
)  # table = "gdc-bq-sample.integration", version = "all_v2")
print(r3_1)
