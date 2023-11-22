from cdapython import unique_terms
from tests.global_settings import host, project


def test_unique_paginator():
    projlist = []
    for i in unique_terms(
        col_name="sex",
        host=host,
    ).paginator(to_list=True):
        projlist.extend(i)
    assert len(projlist) > 0
