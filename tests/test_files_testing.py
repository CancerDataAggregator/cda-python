from cdapython import Q

r = Q('id = "TCGA-E2-A10A"').run(host="http://35.192.60.10:8080/")
print(r.pretty_print())
