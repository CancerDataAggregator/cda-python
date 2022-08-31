from cdapython import Q

# print(Q("days_to_birth <= -50 * 365").to_json())

print(Q("days_to_birth <= 50*-365 AND >= 20*-365").to_json())

# myquery = Q('primary_diagnosis_site = "brain"').mutation.count.run()
