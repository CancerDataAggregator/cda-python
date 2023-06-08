from cdapython import Q
from tests.global_settings import localhost, table_dev

for i in (
    Q("sex = 'male'").set_verbose(False).set_host(host=localhost).set_project(table_dev)
):
    print(i)
