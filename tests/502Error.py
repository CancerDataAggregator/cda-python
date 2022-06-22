from cdapython import Q
from tests.global_settings import localhost, host

# q1 = Q("ResearchSubject.Diagnosis.age_at_diagnosis > 50*365")
# q2 = Q('ResearchSubject.associated_project = "TCGA-OV"').file
# a = q2.AND(q1)


# a = Q(
#     'ResearchSubject.primary_diagnosis_site IN ("uterus", "uterus, NOS", "Cervix uteri", "Chest-Abdomen-Pelvis, Leg, TSpine")'
# )

# t = Q(
#     "ResearchSubject.primary_diagnosis_site =  'Bones, joints and articular cartilage of other and unspecified sites' "
# )
# print(a.to_json())
# Q("ResearchSubject.Diagnosis.morphology = '84%'").researchsubject.run(
#     host="http://localhost:8080"
# ).to_dict()


# d = Q(
#     """
#     ResearchSubject.primary_diagnosis_site = "uterus, NOS" OR
#     ResearchSubject.primary_diagnosis_site = "uterus" OR
#     ResearchSubject.primary_diagnosis_site = "Cervix" OR
#     ResearchSubject.primary_diagnosis_site = "Cervix uteri"
# """
# ).researchsubject.count.run(host=host)


d = Q(
    """
      ResearchSubject.primary_diagnosis_site = "uterus, NOS" OR 
      ResearchSubject.primary_diagnosis_site = "uterus" OR 
      ResearchSubject.primary_diagnosis_site = "Cervix" OR 
      ResearchSubject.primary_diagnosis_site = "Cervix uteri
      "
"""
).researchsubject.run(show_sql=True, host=host, limit=1000)
print(d.to_list())
# print(a.researchsubject.count.run(host=localhost))
# q = q1.AND(q2)

# data = q.researchsubject.count.run(host="http://localhost:8080")

# print(data)
