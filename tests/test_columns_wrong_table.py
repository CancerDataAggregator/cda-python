import pytest

from cdapython import columns


def test_basic_integration():
    with pytest.raises(ValueError):
        cols = columns(table="data").to_list()
        assert cols is None
