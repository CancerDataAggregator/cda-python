from cdapython import Q, columns

Q.set_default_project_dataset("broad-dsde-dev.cda_dev")
Q.set_host_url("https://cancerdata.dsde-dev.broadinstitute.org/")
Q.get_host_url()
Q.get_default_project_dataset()

print(columns().to_list())
