from cdapython import columns
from tests.global_settings import integration_host

"""
fieldName,endpoint,description
"""


def test_columns():
    print(columns(verify=False).to_list())


test_columns()
