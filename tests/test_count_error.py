from cdapython import Q
q1 = Q('ResearchSubject.Specimen.primary_disease_type = "Nevi and Melanomas"')

q = q1
r = q.counts(host="http://local")

print(r)