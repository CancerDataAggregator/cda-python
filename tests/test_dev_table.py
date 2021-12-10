from cdapython import Q
q = Q('id = "TCGA-13-1409"') # note the double quotes for the string value
r = q.run(table = "gdc-bq-sample.dev", version = "all_v1")