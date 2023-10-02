from global_settings import host

from cdapython import Q

age1 = Q("age_at_diagnosis >= 40*365")
age2 = Q("age_at_diagnosis <= 45*365")
female = Q('sex = "female"')
brca = Q('associated_project = "TCGA-BRCA"')
normals = Q('source_material_type = "Blood Derived Normal"')
tumors = Q('source_material_type = "Primary Tumor"')

q = normals.FROM(tumors.AND(brca.AND(female.AND(age1.AND(age2)))))
r = q.researchsubject.count.run(host=host)
print(r)
