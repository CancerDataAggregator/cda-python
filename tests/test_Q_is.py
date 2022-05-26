from cdapython import Q

# print(Q("sex is not null").to_json())

print(Q("sex = 'male' and sex = 'female'").to_json())
