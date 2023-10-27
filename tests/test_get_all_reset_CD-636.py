from typing import cast
from cdapython import unique_terms
from cdapython.results.factories import COLLECT_RESULT
from cdapython.results.factories.collect_result import CollectResult
from cdapython.results.factories.result_factory import ResultFactory
from tests.global_settings import host


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
