from cdapython import columns
from cdapython import unique_terms


def test_basic_integration():
    cols = columns()
    assert "race" in cols
     

def test_unique_terms():
    terms = unique_terms('sex')
    assert "female" in terms