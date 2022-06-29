from cdapython import Q
from tests.global_settings import host


# def test_not() -> None:
#     Q('sex NOT LIKE "m%"').subject.count.run(host=host)


# print(
#     Q(
#         'ResearchSubject.primary_diagnosis_site = "uterus" OR ResearchSubject.primary_diagnosis_condition = "Uterine Corpus Endometrial Carcinoma"'
#     ).researchsubject.count.to_json()
# )


# Query1 = Q('ResearchSubject.primary_diagnosis_site = "uterus"')
# Query2 = Q(
#     'ResearchSubject.primary_diagnosis_condition = "Uterine Corpus Endometrial Carcinoma"'
# )

# print(Query1.Or(Query2).researchsubject.count.to_json())
# print(
#     Q(
#         "ResearchSubject.id IN ['C0EF0C13-3109-47CF-9BA4-076AB7EB7660',' 6AA44F89-FCE7-46FE-A1CB-874CD5EFA4A4']"
#     ).to_json()
# )
#         0   10  4     40    10  4     0
a = Q('sex = "male" AND sex = "female" AND NOT sex = "unknown"').run()
print(a)

# print(Q('sex = "male" or sex = "female" AND NOT sex = "unknown"').to_json())

print(Q('sex = "m%"').to_json())
print(Q('sex != "m%"').to_json())
print(Q('sex <> "m%"').to_json())
