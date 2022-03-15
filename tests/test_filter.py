from cdapython import Q
from tests.global_settings import host

q = Q('id = "TCGA-13-1409"')  # note the double quotes for the string value
r = q.run(host=host, verbose=False)

# r.to_DataFrame().to_csv("test.tsv", sep="\t")
