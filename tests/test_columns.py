from cdapython import columns, Q


def test_columns():
    Q.set_host_url("http://34.71.0.127:8080")
    cols = columns()
    assert isinstance(cols, list) is True


test_columns()
