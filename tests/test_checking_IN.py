from unittest import mock

from pandas import DataFrame

from cdapython import Q
from cdapython.results.result import Result
from tests.fake_result import FakeResultData
from tests.global_settings import host, table

result = [
    {
        "id": "GENIE-DFCI-007281",
        "identifier": [{"system": "GDC", "value": "GENIE-DFCI-007281"}],
        "species": "homo sapiens",
        "sex": "male",
        "race": "white",
        "ethnicity": "not hispanic or latino",
        "days_to_birth": -16071,
        "subject_associated_project": ["GENIE-DFCI"],
        "vital_status": "Not Reported",
        "days_to_death": None,
        "cause_of_death": None,
    }
]

fake = FakeResultData(result)
fake_result = Result(
    api_response=fake.api_response,
    query_id=fake.query_id,
    offset=fake.offset,
    limit=fake.limit,
    api_instance=fake.api_instance,
    show_sql=fake.show_sql,
    show_count=fake.show_count,
    format_type=fake.format_type,
)


@mock.patch("cdapython.Q.run", return_value=fake_result)
def test_checking_test(_):
    q1 = Q(
        "id IN ['C0EF0C13-3109-47CF-9BA4-076AB7EB7660','6AA44F89-FCE7-46FE-A1CB-874CD5EFA4A4']"
    ).AND(Q('sex = "male"'))
    print(q1)
    assert q1.to_dict()["l"]["node_type"] == "IN"
    r = q1.run(host=host, table=table)
    print(r.to_list())
    assert isinstance(r.to_list(), list) is True
    assert isinstance(r.to_dataframe(), DataFrame) is True


test_checking_test()
