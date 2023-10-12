from cdapython import (
    Q,
    get_default_project_dataset,
    get_host_url,
    set_default_project_dataset,
    set_host_url,
    set_table_version,
)
from tests.global_settings import host, project

# def test_set_new_host():


# print(columns().to_dataframe().to_csv("test.csv"))


# test_set_new_host()

Tsite = Q('treatment_anatomic_site = "Cervix"')
Dsite = Q('primary_diagnosis_site = "%uter%" OR primary_diagnosis_site = "%cerv%"')
ALLDATA = Tsite.OR(Dsite)
print(ALLDATA.researchsubject.count.set_host(host).run())
