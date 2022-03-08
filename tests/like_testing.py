from cdapython import Q
q = Q('ResearchSubject.primary_disease_type = "Lung%"')
r = q.run(host='http://localhost:8080')
