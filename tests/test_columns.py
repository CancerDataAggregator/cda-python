from cdapython import columns, Q


def test_columns():
    Q.set_host_url("http://35.192.60.10:8080")
    cols = columns()
    assert isinstance(cols, list) is True
