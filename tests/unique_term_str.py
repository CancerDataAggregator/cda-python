from cdapython import unique_terms, Q

Q.set_default_project_dataset("broad-dsde-dev.cda_dev")
Q.set_host_url("https://cancerdata.dsde-dev.broadinstitute.org/")
Q.get_host_url()
# from tests.global_settings import localhost


print(
   unique_terms("primary_diagnosis_site", show_counts = True).to_dataframe(search_fields= "*", search_value = "gland")
)
