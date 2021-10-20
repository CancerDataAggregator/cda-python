from cdapython.utility import query

q = query(
    'ResearchSubject.associated_project = "TCGA-OV" AND ResearchSubject.Diagnosis.age_at_diagnosis != 21550'
)

r = q.run()

print(r)
