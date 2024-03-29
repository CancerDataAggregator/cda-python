import sys

from cdapython import Q

sex = Q('sex = "female"')
cancer = Q('ResearchSubject.primary_diagnosis_condition = "Breast Invasive Carcinoma"')
ageL = Q("days_to_birth <= -30*365")
ageU = Q("days_to_birth >= -45*365")

q1 = sex.AND(cancer.AND(ageL.AND(ageU)))

r1 = q1.run(async_call=True)

tmp = r1[0]
# sleep(11)

r2 = q1.run(async_call=True, format_type="tsv")


print(sys.getsizeof(r2))

# r2.pretty_print(0)
