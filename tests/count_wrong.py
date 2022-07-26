from global_settings import host, integration_host
from cdapython import Q

q = Q('id="TCGA-E2-A10A"')  # note the double quotes for the string value

r = q.count.run(host=integration_host)
print(r)
