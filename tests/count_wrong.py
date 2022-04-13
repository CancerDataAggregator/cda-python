from cdapython import Q
from global_settings import localhost
q = Q('id = "TCGA-E2-A10A"') # note the double quotes for the string value

r = q.run(host=localhost)
print(r)