from cdapython import Q, columns
from tests.global_settings import table, host

Q.set_host_url(host)
Q.set_default_project_dataset(table)
Q.get_host_url()
Q.get_default_project_dataset()

print(columns().to_list())
