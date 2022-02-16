from cdapython import Q
import sys

sex = Q('sex = "female"')
cancer = Q('ResearchSubject.primary_diagnosis_condition = "Breast Invasive Carcinoma"')
ageL = Q("days_to_birth <= -30*365")
ageU = Q("days_to_birth >= -45*365")

q1 = sex.And(cancer.And(ageL.And(ageU)))

r1 = q1.run()

tmp = r1[0]
# sleep(11)
print("cache")
r2 = q1.run()

print(sys.getsizeof(r2))

# r2.pretty_print(0)
