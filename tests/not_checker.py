from cdapython.utility import query


q = query(
    'sex = "female" AND primary_diagnosis_condition = "Breast Invasive Carcinoma" AND days_to_birth <= -30*365 AND days_to_birth >= -45*365'
)

r = q.run()

print(r)
