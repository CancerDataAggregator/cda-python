from global_settings import host, localhost, table

from cdapython import Q

d = Q('ResearchSubject.Specimen.specimen_type = "slide"').specimen.run(
    include="""
    id:r_id 
    species:things
    sex:gender
    race:me
    ethnicity:like_race
    days_to_birth:born
    subject_associated_project
    vital_status 
    days_to_death
    cause_of_death 
    identifier
    File.label
    File.data_category
    File.data_type
    File.file_format
    File.data_modality""",
    host=host,
    table=table,
)

print(d.to_list())
print(d.to_dataframe())

print(d.join_as_str(key="me", delimiter=","))
