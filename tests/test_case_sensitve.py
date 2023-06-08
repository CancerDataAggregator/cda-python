from cdapython import Q
from tests.global_settings import host

q = Q("days_to_death  IN (10,20)")


# note the double quotes for the string value
# r3_1 = q.run(
#     host=host, show_sql=True
# )  # table = "gdc-bq-sample.integration", version = "all_v2")
print(q.to_json())
