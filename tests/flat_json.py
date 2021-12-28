from cdapython import Q

q = Q('id = "TCGA-E2-A10A"')
q1 = q.run(host="http://localhost:8080", verbose=False)
print(q1)
