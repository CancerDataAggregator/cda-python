from cdapython import Q

q1 = Q('ResearchSubject.primary_diagnosis_site = "Kidney"')
r1 = q1.run(offset=500, async_call=True)

print(r1)
