from cdapython import Q, constantVariables
from global_settings import host, integration_host

q = Q('id = "TCGA-E2-A10A"')  # note the double quotes for the string value

r = q.counts(host=integration_host, table=constantVariables.file_table_version)
print(r.pretty_print())
