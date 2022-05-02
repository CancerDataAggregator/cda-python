from cdapython import Q

q1 = Q(
    'ResearchSubject.primary_diagnosis_condition = "Ovarian Serous Cystadenocarcinoma"'
)
q2 = Q('ResearchSubject.identifier.system = "PDC"')
q3 = Q('ResearchSubject.identifier.system = "GDC"')

q = q3.From(q1.And(q2))

print(q.to_json())
