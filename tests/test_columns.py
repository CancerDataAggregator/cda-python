from cdapython import Q, columns
from tests.global_settings import host, integration_host, table

"""
fieldName,endpoint,description
"""


def test_columns():

    print(
        columns(host=integration_host, version="all_Subjects_v3_1_final").to_dataframe()
    )


test_columns()
