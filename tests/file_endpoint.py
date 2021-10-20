from cdapython import Q

q1 = Q('ResearchSubject.identifier = "GDC"')
q2 = Q('ResearchSubject.Specimen.source_material_type = "Primary Tumor"')
q3 = Q('ResearchSubject.Specimen.source_material_type = "Blood Derived Normal"')
q = q1.And(q2.Or(q3))
r = q.run()
print()
