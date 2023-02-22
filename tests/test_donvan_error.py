from cdapython import Q
from unittest import mock
from pandas import DataFrame
from tests.fake_result import FakeResultData
from cdapython.results.count_result import CountResult

result = [
    {
        "total": 65,
        "files": 45342,
        "system": [
            {"system": "GDC", "count": 65},
            {"system": "PDC", "count": 65},
            {"system": "IDC", "count": 65},
        ],
        "sex": [{"sex": "male", "count": 47}, {"sex": "female", "count": 18}],
        "race": [
            {"race": "white", "count": 38},
            {"race": "not reported", "count": 26},
            {"race": "asian", "count": 1},
        ],
        "ethnicity": [
            {"ethnicity": "not hispanic or latino", "count": 26},
            {"ethnicity": "not reported", "count": 35},
            {"ethnicity": "hispanic or latino", "count": 4},
        ],
        "cause_of_death": [
            {"cause_of_death": "Not Reported", "count": 63},
            {"cause_of_death": "Cancer Related", "count": 2},
        ],
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
def test_donvan_error(a):
    q1 = Q('ResearchSubject.Diagnosis.stage = "Stage I"')
    q2 = Q('ResearchSubject.Diagnosis.stage = "Stage II"')
    q3 = Q("ResearchSubject.primary_diagnosis_site = 'Kidney'")
    q_diag = q1.OR(q2)
    q = q_diag.AND(q3)
    # print(q.counts.run())
    qsub = q.subject.count.run()
    assert isinstance(qsub.to_list(), list) is True
    assert isinstance(qsub.to_dataframe(), DataFrame) is True


test_donvan_error()
