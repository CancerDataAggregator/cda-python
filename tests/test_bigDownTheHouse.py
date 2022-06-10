from cdapython import Q
from tests.global_settings import host

q1 = Q('File.associated_project = "tcga_brca"')
q2 = Q('File.associated_project = "TCGA-BRCA"')
q3 = Q("Subject.days_to_birth < -50*365")
q4 = Q('File.data_category = "Imaging"')
q = q4.AND(q3.AND(q1.OR(q2)))
print(q)
t = q.file.run(host=host)

print(t)
# print(t.to_dataframe().head())
