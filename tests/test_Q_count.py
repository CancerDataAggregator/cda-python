from unittest.mock import patch

from cdapython import Q
from cdapython.results.count_result import CountResult

try:
    from tests.fake_result import FakeResultData
    from tests.global_settings import integration_table, localhost
except Exception as _:
    from fake_result import FakeResultData
    from global_settings import integration_table, localhost

result = [
    {
        "specimen_count": 406882,
        "treatment_count": 16332,
        "diagnosis_count": 46839,
        "mutation_count": 5220,
        "researchsubject_count": 53363,
        "subject_count": 45988,
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


@patch("cdapython.Q.run", return_value=fake_result)
def test_Q_count(_):
    test_count = Q(
        'vital_status IS NULL OR age_at_diagnosis = 0 AND sex = "male" OR sex = "female" '
    )

    box = test_count.count.to_list()
    test_dict = {
        "specimen_count": 406882,
        "treatment_count": 16332,
        "diagnosis_count": 46839,
        "mutation_count": 5220,
        "researchsubject_count": 53363,
        "subject_count": 45988,
    }
    for i in box:
        assert i == test_dict


test_Q_count()
