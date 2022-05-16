from cdapython import columns, Q
from tests.global_settings import host


def test_columns():
    Q.set_host_url(host)
    cols = columns().to_list()
    assert isinstance(cols, list) is True
