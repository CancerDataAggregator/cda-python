from cdapython import Q
q1 = Q('ResearchSubject.Diagnosis.Treatment.treatment_type = "Radiation Therapy, NOS"')
q2 = Q('ResearchSubject.identifier.system = "PDC"')
q3 = Q('ResearchSubject.identifier.system = "GDC"')
q = q2.From(q1.And(q3))


q1 = Q('ResearchSubject.Diagnosis.Treatment.treatment_type = "Radiation Therapy, ADB"')
q2 = Q('ResearchSubject.identifier.system = "PDC"')
q3 = Q('ResearchSubject.identifier.system = "GDC"')
q = q2.From(q1.And(q3))
r = q.run()

print(r)
