from unittest import mock

from pandas import DataFrame

from cdapython import Q
from cdapython.results.count_result import CountResult
from tests.fake_result import FakeResultData
from tests.global_settings import host, project

result = [
    {
        "specimen_count": 755924,
        "treatment_count": 32748,
        "diagnosis_count": 86799,
        "researchsubject_count": 99178,
        "subject_count": 85438,
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
def test_glb_count(a) -> None:
    r = Q('sex = "male" OR sex = "female"')
    q1 = r.count.run(host=host, limit=100, table=project)
    print(q1)
    # print(q1.to_list())
    assert isinstance(q1.to_list(), list) is True
    assert isinstance(q1.to_dataframe(), DataFrame) is True


test_glb_count()
