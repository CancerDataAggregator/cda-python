from cdapython import Q, set_default_project_dataset, set_host_url, set_table_version

set_default_project_dataset("gdc-bq-sample.dev")
set_host_url("http://35.192.60.10:8080")
set_table_version("all_Subjects_v3_0_final")

a = Q('sex = "%" AND researchsubject_identifier_system = "IDC"').run().get_all()
