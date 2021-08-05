from cdapython import columns
from cdapython import unique_terms
import pytest

def test_basic_integration():
    cols = columns()
    assert "race" in cols


def test_unique_terms():
    # pytest.set_trace()
    terms = unique_terms('sex', 'GDC')
    assert "female" in terms
