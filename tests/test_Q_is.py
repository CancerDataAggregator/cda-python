from cdapython import Q

# print(Q("sex is not null").to_json())

# print(
#     Q(
#         "ResearchSubject.id IN ['C0EF0C13-3109-47CF-9BA4-076AB7EB7660',' 6AA44F89-FCE7-46FE-A1CB-874CD5EFA4A4']"
#     ).to_json()
# )
#         0   10  4     40    10  4     0
# print(Q('sex = "male" and sex = "female" AND NOT sex = "unknown"').to_json())

print(Q('sex = "male" or sex = "female" AND NOT sex = "unknown"').to_json())
