import pytest

from cdapython import columns


def test_basic_integration():
    with pytest.raises(AttributeError):
        cols = columns(version="data").to_list()
        assert cols is None
