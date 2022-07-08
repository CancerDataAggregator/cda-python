from cdapython import columns, unique_terms
from tests.global_settings import host, table


def test_basic_integration() -> None:
    cols = columns(host=host, table=table)
    assert "race" in cols


def test_unique_terms() -> None:
    terms = unique_terms("sex", "GDC", host=host, table=table)
    assert "female" in terms
