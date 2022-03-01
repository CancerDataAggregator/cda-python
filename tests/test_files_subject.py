from cdapython import Q

q = Q('Subject.id = "TCGA-13-1409"')  # note the double quotes for the string value
r = q.files(host="http://localhost:8080")
print(r)