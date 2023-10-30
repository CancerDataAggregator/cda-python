from cdapython import columns
from tests.global_settings import host


def test_columns_dataframe_search():
    df = columns(host=host).to_dataframe(
        search_fields=["description", "fieldName"], search_value="diagnosis"
    )
    for _, row in df.iterrows():
        df_output = (
            row["description"].find("dog") > -1 or row["fieldName"].find("dog") > -1
        )
        assert df_output is False
        df_output = (
            row["description"].find("diagnosis") > -1
            or row["fieldName"].find("diagnosis") > -1
        )
        assert df_output is True

    assert "description" in df
    assert "fieldName" in df
    assert df is not None
