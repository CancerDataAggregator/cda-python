from cdapython import Q

age1 = Q("ResearchSubject.Diagnosis.age_at_diagnosis >= 40*365")
age2 = Q("ResearchSubject.Diagnosis.age_at_diagnosis <= 45*365")
female = Q('sex = "female"')
brca = Q('ResearchSubject.associated_project = "TCGA-BRCA"')
bams = Q('ResearchSubject.Specimen.File.file_format = "BAM"')
normals = Q('ResearchSubject.Specimen.source_material_type = "Blood Derived Normal"')
tumors = Q('ResearchSubject.Specimen.source_material_type = "Primary Tumor"')

q = normals.From(tumors.And(brca.And(bams.And(female.And(age1.And(age2))))))
r = q.run()
print(r)
r.next_page()
print(r)
