from cdapython import Q, columns
from tests.global_settings import host, project

# q1 = Q("ResearchSubject.Diagnosis.age_at_diagnosis > 50*365")
# q2 = Q('ResearchSubject.associated_project = "TCGA-OV"')

# print(columns().df_to_table())

Q("subject_associated_project_associated_project = 'TCGA-OV' ").researchsubject.run()

df = columns(host=host).to_dataframe()
print(df[df["fieldName"].str.contains("associated_project")])


# def test_conversion() -> None:
#     q1 = Q("age_at_diagnosis > 50 * 365").diagnosis
#     q2 = Q('associated_project = "TCGA-OV"').researchsubject
#     q = q1.AND(q2)

#     r = q.set_host(host).set_project(project).run().to_dataframe().head()
#     print(r)


# test_conversion()
