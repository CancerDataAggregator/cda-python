from cdapython import Q, columns
from tests.global_settings import integration_host, integration_table

def test_set_new_host():
    Q.set_host_url(integration_host)
    Q.set_default_project_dataset(integration_table)
    Q.get_host_url()
    Q.get_default_project_dataset()

    print(columns().to_list())
