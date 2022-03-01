from cdapython import Q
q1 = Q('File.associated_project = "tcga_brca"')
q2 = Q('File.associated_project = "TCGA-BRCA"')
q3 = Q('days_to_birth < -50*365')
q4 = Q('File.data_category = "Imaging"')
q = q4.And(q3.And(q1.Or(q2)))
print(q)