from cdapython import columns
from tests.global_settings import host

"""
fieldName,endpoint,description
"""


def test_columns():
    print(columns(host=host, verify=False).to_list())


test_columns()
