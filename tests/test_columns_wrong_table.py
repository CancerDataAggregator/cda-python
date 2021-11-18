from cdapython import columns
import pytest


def test_basic_integration():
    with pytest.raises(ValueError):
        cols = columns(table="data")
        assert cols is None


test_basic_integration()
