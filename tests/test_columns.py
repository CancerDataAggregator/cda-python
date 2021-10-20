from cdapython import columns


def test_basic_integration():
    cols = columns()
    assert isinstance(cols, list) is True
