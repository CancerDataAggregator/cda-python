from cdapython import Q

# print(
#     Q(
#         'ResearchSubject.primary_diagnosis_site = "uterus" OR ResearchSubject.primary_diagnosis_condition = "Uterine Corpus Endometrial Carcinoma"'
#     ).researchsubject.count.to_json()
# )


Query1 = Q('ResearchSubject.primary_diagnosis_site = "uterus"')
Query2 = Q(
    'ResearchSubject.primary_diagnosis_condition = "Uterine Corpus Endometrial Carcinoma"'
)

print(Query1.OR(Query2).researchsubject.count.to_json())
