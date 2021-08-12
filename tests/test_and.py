from cdapython import Q

q1 = Q('ResearchSubject.Diagnosis.age_at_diagnosis > 50*365')
q2 = Q('ResearchSubject.associated_project = "TCGA-OV"')

q = q1.And(q2)
r = q.run()

assert r.count == 461
