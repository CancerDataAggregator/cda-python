from cdapython import Q

# print(Q("days_to_birth <= -50 * 365").to_json())

print(Q("days_to_birth <= 50*-365 AND days_to_birth >= 20*-395"))

# myquery = Q('primary_diagnosis_site = "brain"').mutation.count.run()
