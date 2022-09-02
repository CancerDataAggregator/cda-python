from cdapython import Q, columns
from tests.global_settings import host, table
from cdapython.results.result import Result
from unittest import mock
from pandas import DataFrame
from tests.fake_result import FakeResultData

result = [
    {
        "id": "TCGA-13-1409",
        "identifier": [
            {"system": "GDC", "value": "TCGA-13-1409"},
            {"system": "PDC", "value": "TCGA-13-1409"},
            {"system": "IDC", "value": "TCGA-13-1409"},
        ],
        "species": "homo sapiens",
        "sex": "female",
        "race": "white",
        "ethnicity": "not hispanic or latino",
        "days_to_birth": -26836,
        "subject_associated_project": ["tcga_ov", "CPTAC-TCGA", "TCGA-OV"],
        "vital_status": "Dead",
        "days_to_death": 1742,
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
def test_ssl_q(a) -> None:
    r = Q('id = "TCGA-13-1409"')
    q = r.run(verify=False, host=host, table=table)
    print(q.to_list())
    # print(host, table)
    assert q.count == 1
    assert isinstance(q.to_list(), list) is True
    assert isinstance(q.to_dataframe(), DataFrame) is True


print(host, table)
columns(verify=False, host=host, table=table, verbose=True)
