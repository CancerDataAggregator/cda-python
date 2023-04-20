from cdapython import Q
from tests.global_settings import host, project

q = Q('primary_disease_type = "Lung%"').set_project(project)
print(q.to_json())

q = q.run(host=host, table=project).to_dataframe()


print(q.head())
