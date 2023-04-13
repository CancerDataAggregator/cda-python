from unittest import mock

from pandas import DataFrame

from cdapython import Q
from cdapython.results.result import Result
from tests.fake_result import FakeResultData

result = [
    {
        "id": "09CO022",
        "identifier": [
            {"system": "GDC", "value": "09CO022"},
            {"system": "PDC", "value": "09CO022"},
            {"system": "IDC", "value": "09CO022"},
        ],
        "species": "homo sapiens",
        "sex": "female",
        "race": "black or african american",
        "ethnicity": "not hispanic or latino",
        "days_to_birth": None,
        "subject_associated_project": ["CPTAC-2", "cptac_coad"],
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
def test_ssl(a):
    q1 = Q('researchsubject_id = "c5421e34-e5c7-4ba5-aed9-146a5575fd8d"')

    q1.run(verify=False)

    qsub = q1.subject.run()
    assert isinstance(qsub.to_list(), list) is True
    assert isinstance(qsub.to_dataframe(), DataFrame) is True
