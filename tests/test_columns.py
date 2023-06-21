from cdapython import columns
from tests.global_settings import localhost

"""
fieldName,endpoint,description
"""


def test_columns():
    print(columns(host=localhost, verify=False).to_list())


test_columns()
