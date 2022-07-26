import pandas
from cdapython import Q

Q.set_default_project_dataset("broad-dsde-dev.cda_dev")
Q.set_host_url("https://cancerdata.dsde-dev.broadinstitute.org/")

print(Q.get_host_url())
print(Q.get_default_project_dataset())
s = Q(
    'ResearchSubject.Specimen.specimen_type= "slide" OR file.data_type = "Slide Image"'
).specimen.file.run(
    filter="""
File.id  
File.identifier.system  
File.label  
File.data_category 
File.data_type  
id  
identifier.system  
species  
sex  
race  
subject_associated_project 
ResearchSubject.id 
ResearchSubject.identifier.system 
ResearchSubject.member_of_research_project 
ResearchSubject.primary_diagnosis_condition  
ResearchSubject.primary_diagnosis_site  
ResearchSubject.Diagnosis.identifier.system 
ResearchSubject.Specimen.id  
ResearchSubject.Specimen.identifier.system  
ResearchSubject.Specimen.identifier.value  
ResearchSubject.Specimen.associated_project  
ResearchSubject.Specimen.days_to_collection  
ResearchSubject.Specimen.primary_disease_type  
ResearchSubject.Specimen.anatomical_site  
ResearchSubject.Specimen.source_material_type  
ResearchSubject.Specimen.specimen_type  
ResearchSubject.Specimen.derived_from_specimen  
ResearchSubject.Specimen.derived_from_subject
""",
    show_sql=True,
)
s = Q("sex = 'male'").run()
df = pandas.DataFrame()
id(df)
p = s.auto_paginator(to_df=True, limit=10000,host_df=df)


print(p)
