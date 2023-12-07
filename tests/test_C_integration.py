from pytest import fail

from cdapython import Q, columns, unique_terms
from tests.global_settings import host, project


def test_basic_integration() -> None:
    cols = columns(host=host, description=False).to_list()
    assert "race" in cols


def test_unique_terms() -> None:
    terms = unique_terms(col_name="sex", system="GDC", host=host, show_counts=True)
    list_terms = terms.to_list()
    flat_terms = [list(i.values())[0] for i in list_terms]
    assert "female" in flat_terms

    if terms:
        filtered_list = list(filter(lambda obj: obj["sex"] == "female", terms))

        # filtered_list = [i for i in terms if i["sex"] == "female"]
        assert len(filtered_list) == 1
        assert filtered_list[0]["count"] > 0
    else:
        assert fail("There was no terms returned")


test_unique_terms()
