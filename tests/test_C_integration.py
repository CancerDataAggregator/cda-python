from cdapython import columns, unique_terms
from tests.global_settings import integration_host, integration_table


def test_basic_integration() -> None:
    cols = columns(
        host=integration_host, table=integration_table, description=False
    ).to_list()
    assert "race" in cols


def test_unique_terms() -> None:
    terms = unique_terms(
        "sex", "GDC", host=integration_host, table=integration_table
    ).to_list()
    assert "female" in terms
