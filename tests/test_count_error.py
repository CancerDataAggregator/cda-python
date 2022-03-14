from cdapython import Q

q1 = Q('ResearchSubject.Specimen.primary_disease_type = "Nevi and Melanomas"')

q = q1
print(q)
r = q.counts(host="http://localhost:8080")

print(r)
