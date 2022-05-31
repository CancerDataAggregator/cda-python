from collections import Counter

import pandas as pd

from cdapython import Q
from tests.global_settings import host

sex = Q('sex = "female"')
cancer = Q('ResearchSubject.primary_disease_type = "Breast Invasive Carcinoma"')
ageL = Q("days_to_birth <= -30*365")
ageU = Q("days_to_birth >= -45*365")

q1 = sex.And(cancer.And(ageL.And(ageU)))

print(q1.researchsubject.count.run(host=host))

# 0 r3 = q1.run(host="http://localhost:8080")


# print(r3)
