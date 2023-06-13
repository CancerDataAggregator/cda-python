from pytest import raises

from cdapython import columns


def test_basic_integration() -> None:
    cols = columns()
    if cols is not None:
        cols.to_list()
    else:
        assert cols is None


test_basic_integration()
