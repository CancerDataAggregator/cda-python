from cdapython import Q

q = Q("ResearchSubject.Diagnosis.age_at_diagnosis > 50*365").to_json()

print(q)
