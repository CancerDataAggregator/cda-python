"""
Testing unique_term pagination using paginator and get_all
"""
from cdapython import unique_terms
from tests.global_settings import host


def test_unique_paginator():
    projlist = []
    terms = unique_terms(col_name="sex", host=host, show_counts=True)
    for list_of_terms in terms.paginator(to_list=True):
        assert all("count" in term_dict for term_dict in list_of_terms) is True
        projlist.extend(list_of_terms)

    assert len(projlist) > 0
    assert any("count" in d for d in projlist) is True


def test_unique_paginator_show_count_false():
    projlist = []
    terms = unique_terms(col_name="sex", host=host, show_counts=False)
    for i in terms.paginator(to_list=True):
        projlist.extend(i)

    assert len(projlist) > 0
    assert any("count" in d for d in projlist) is False


def test_unique_paginator_show_count_unset():
    projlist = []
    terms = unique_terms(col_name="sex", host=host)
    for i in terms.paginator(to_list=True):
        projlist.extend(i)

    assert len(projlist) > 0
    assert any("count" in d for d in projlist) is False


def test_unique_list():
    projlist = (
        unique_terms("primary_diagnosis_site").get_all(show_counts=True).to_dataframe()
    )
    print(projlist)
    assert any("count" in d for d in projlist) is True


def test_unique_list_turn_off_show_counts():
    projlist = (
        unique_terms("primary_diagnosis_site").get_all(show_counts=False).to_dataframe()
    )
    print(projlist)
    assert all("count" in d for d in projlist) is False


def test_unique_list_unset_show_counts():
    projlist = unique_terms("primary_diagnosis_site").get_all().to_dataframe()
    print(projlist)
    assert all("count" in d for d in projlist) is False
