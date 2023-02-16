from cdapython import Q, unique_terms

Q.set_default_project_dataset("gdc-bq-sample.dev")
Q.set_host_url("http://35.192.60.10:8080")
Q.set_table_version("all_Subjects_v3_0_final")

a = Q('var a = sex = "male" AND race = "%or%"').run().get_all()

print(unique_terms("race").df_to_table())
print(a.df_to_table())
