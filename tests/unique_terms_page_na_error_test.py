from global_settings import integration_host, localhost, project

from cdapython import unique_terms

df = unique_terms(
    "subject_id", system="GDC", page_size=10000, host=integration_host, table=project
).get_all()

for index, i in enumerate(df.to_list()):
    print(index, i)
