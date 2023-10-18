from cdapython import unique_terms
from tests.global_settings import host


def test_data_type_get_all():
    data_type = unique_terms("data_type").run(host=host, limit=10)
    assert len(data_type.to_dataframe()) == 10

    all_data_type = data_type.get_all(limit=20)

    assert all_data_type.total_row_count == len(all_data_type)
