from cdapython import Q
from tests.global_settings import integration_table, localhost

sex = Q('sex = "female"')
cancer = Q('primary_disease_type = "Breast Invasive Carcinoma"')
ageL = Q("days_to_birth <= -30*365")
ageU = Q("days_to_birth >= -45 * 365")

q1 = sex.AND(cancer.AND(ageL.AND(ageU)))

print(q1.to_json())


a = Q(
    """
        sex = "female"
        AND 
        primary_disease_type = "Breast Invasive Carcinoma"
        AND
        days_to_birth >= -30 * 365
        AND
        days_to_birth = 5 * 5 
    """
)

print(a.to_json())


print(a.run(host=localhost, table=integration_table))
# 0 r3 = q1.run(host="http://localhost:8080")


# print(r3)
