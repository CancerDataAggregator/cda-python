from cdapython import Q
from unittest import mock
from pandas import DataFrame
from tests.supermock import Result_Type, SuperMock

result = [
    {
        "total": 65,
        "files": 45342,
        "system": [
            {"system": "IDC", "count": 65},
            {"system": "PDC", "count": 65},
            {"system": "GDC", "count": 65},
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


@mock.patch("cdapython.Q.run", return_value=result)
def test_donvan_error(a):
    q1 = Q('ResearchSubject.Diagnosis.stage = "Stage I"')
    q2 = Q('ResearchSubject.Diagnosis.stage = "Stage II"')
    q3 = Q("ResearchSubject.primary_diagnosis_site = 'Kidney'")
    q_diag = q1.OR(q2)
    q = q_diag.AND(q3)
    # print(q.counts.run())
    qsub = q.subject.count.run(show_sql=True)
    assert isinstance(qsub.to_list(), list) == True
    assert isinstance(qsub.df_to_table(), DataFrame) == True


test_donvan_error()
