from cdapython import Q
import json

sex = Q('sex = "female"')
cancer = Q('ResearchSubject.primary_disease_type = "Breast Invasive Carcinoma"')
ageL = Q("days_to_birth <= -30*365")
ageU = Q("days_to_birth >= -45*365")

q1 = sex.And(cancer.And(ageL.And(ageU)))

r1 = q1.run(host="http://localhost:8080")

r1.pretty_print(0)
