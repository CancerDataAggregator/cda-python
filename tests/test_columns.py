from cdapython import Q, columns
from tests.global_settings import host, table


def test_columns():
    cols = columns(host=host, table=table).to_list()
    assert isinstance(cols, list) is True
