from cdapython import Q

print(Q('ResearchSubject.primary_disease_type = "Lung%"').to_json())
