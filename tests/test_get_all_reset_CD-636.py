from typing import cast

import pytest
from cdapython import unique_terms
from cdapython.results.factories import COLLECT_RESULT
from cdapython.results.factories.collect_result import CollectResult
from cdapython.results.factories.result_factory import ResultFactory
from tests.global_settings import host
from cdapython import Q
from pandas import DataFrame


def test_data_type_get_all():
    data_type = unique_terms("data_type").run(host=host, limit=10)
    assert len(data_type.to_dataframe()) == 10

    all_data_type = data_type.get_all(limit=20)
    all_data_type_copy: "CollectResult" = cast(
        "CollectResult",
        ResultFactory.create_entity(id=COLLECT_RESULT, result_object=all_data_type),
    )
    assert all_data_type.total_row_count == len(all_data_type)

    all_data_type = data_type.get_all(limit=20)

    assert all_data_type.total_row_count == len(all_data_type)
    assert all_data_type_copy == all_data_type


def test_data_type_show_term_count():
    data_type = unique_terms("data_type").run(host=host).get_all(show_term_count=True)
    assert data_type.to_dataframe()["count"]


@pytest.mark.skip(reason="CD-650 Backend always returns counts")
def test_data_type_show_term_count_false():
    with pytest.raises(KeyError):
        data_type = (
            unique_terms("data_type").run(host=host).get_all(show_term_count=False)
        )
        df = data_type.to_dataframe()["count"]
        assert df is None


def test_get_all_with_wrong_result():
    with pytest.raises(AttributeError):
        a = Q("sex = cat").run(host=host).get_all()
        assert a is None


def test_get_with_dataframe():
    a = Q("sex = 'm'").run(host=host).get_all(to_df=True)
    assert isinstance(a, DataFrame)


def test_gell_with_list():
    a = Q("sex = 'm'").run(host=host).get_all(to_list=True)
    assert isinstance(a, list)


def test_gell_with_output_df():
    a = Q("sex = 'm'").run(host=host).get_all(output="full_df")
    assert isinstance(a, DataFrame)


def test_gell_with_output_list():
    a = Q("sex = 'm'").run(host=host).get_all(output="full_list")
    assert isinstance(a, list)


def tests_get_all_with_all():
    a = (
        Q("sex = 'm'")
        .run(host=host)
        .get_all(output="full_list", to_df=True, to_list=True)
    )
    assert isinstance(a, list)


def tests_get_all_with_all_df():
    a = (
        Q("sex = 'm'")
        .run(host=host)
        .get_all(output="full_list", to_df=True, to_list=False)
    )
    assert isinstance(a, DataFrame)


def tests_get_all_with_all_limit():
    a = (
        Q("sex = 'm'")
        .run(limit=10, host=host)
        .get_all(output="full_list", to_df=True, to_list=False, limit=2000)
    )
    assert isinstance(a, list)


# write test for all bellow
# 0 results "sex = cat"
# to_df
# to_list

# show_term_cout
