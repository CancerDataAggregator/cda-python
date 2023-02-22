from cdapython import Q
from tests.global_settings import integration_table, localhost


# def test_set_new_host():
Q.set_host_url(localhost)
Q.set_default_project_dataset(integration_table)
Q.set_table_version("all_Subjects_v3_1_test1")
Q.get_host_url()
Q.get_default_project_dataset()

# print(columns().to_dataframe().to_csv("test.csv"))


# test_set_new_host()

Tsite = Q('treatment_anatomic_site = "Cervix"')
Dsite = Q('primary_diagnosis_site = "%uter%" OR primary_diagnosis_site = "%cerv%"')
ALLDATA = Tsite.OR(Dsite)
print(ALLDATA.researchsubject.count.run())
