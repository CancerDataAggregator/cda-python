from cdapython import Q, columns

from tests.global_settings import host, table, integration_host

"""
fieldName,endpoint,description
"""


def test_columns():

    print(
        columns(host=integration_host, version="all_Subjects_v3_1_test1").to_dataframe(
            search_fields=["fieldName"], search_value="file_id"
        )
    )


test_columns()
