from cdapython import Q
q = Q('ResearchSubject.primary_disease_type = "Lung%"')
print(q)
r = q.run(host='http://localhost:8080')
c = q.counts(host='http://localhost:8080')

print(r)


