from cdapython import query, Q
from tests.global_settings import host
from unittest import mock
from pandas import DataFrame
from tests.fake_result import FakeResultData
from cdapython.results.count_result import CountResult

result = [
    {
        "specimen_count": 354390,
        "treatment_count": 16427,
        "diagnosis_count": 40383,
        "researchsubject_count": 46324,
        "subject_count": 39864,
    }
]

fake = FakeResultData(result)
fake_result = CountResult(
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
def testing_subject(a) -> None:
    q2 = Q("sex = 'male'")
    print(q2.to_json())
    q = q2.subject.count.run(host=host)
    assert isinstance(q.to_list(), list) is True
    assert isinstance(q.to_dataframe(), DataFrame) is True
