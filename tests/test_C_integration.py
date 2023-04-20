from cdapython import columns, unique_terms
from tests.global_settings import host, project


def test_basic_integration() -> None:
    cols = columns(host=host, table=project, description=False).to_list()
    assert "race" in cols


def test_unique_terms() -> None:
    terms = unique_terms("sex", "GDC", host=host, table=project).to_list()
    assert "female" in terms
