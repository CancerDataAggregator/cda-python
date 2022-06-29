from cdapython import Q, columns
from tests.global_settings import host, table


def test_columns():
    Q.set_host_url(host)
    Q.set_table_version(table)
    cols = columns().to_list()
    assert isinstance(cols, list) is True
