from cdapython import columns
from tests.global_settings import integration_host

"""
fieldName,endpoint,description
"""


def test_columns():
    print(
        columns(
            host=integration_host, version="all_Subjects_v3_1_final", verify=False
        ).to_dataframe()
    )


test_columns()
