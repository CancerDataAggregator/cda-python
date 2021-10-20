from cdapython import columns


def test_columns():
    cols = columns()
    assert isinstance(cols, list) is True
