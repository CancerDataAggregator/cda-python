from cdapython import unique_terms
from tests.global_settings import host, project

projlist = []
for i in unique_terms("file_associated_project", host=host, table=project).paginator(
    to_list=True
):
    projlist.extend(i)
print(len(projlist))
