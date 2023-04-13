from pytest import raises

from cdapython import columns


def test_basic_integration() -> None:
    with raises(AttributeError):

        cols = columns(version="data")
        if cols is not None:
            cols.to_list()
        else:
            assert cols is None
