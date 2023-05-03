from unittest.mock import patch

from cdapython import Q
from cdapython.results.count_result import CountResult
from tests.fake_result import FakeResultData
from tests.global_settings import host, project

result = [
    {
        "specimen_count": 432633,
        "treatment_count": 16768,
        "diagnosis_count": 49920,
        "mutation_count": 5135,
        "researchsubject_count": 56604,
        "subject_count": 46551,
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
    test_count = (
        Q('vital_status IS NULL AND sex = "male" OR sex = "female"')
        .count.set_host(host)
        .set_project(project)
        .run()
        .to_list()
    )
    test_dict = {
        "specimen_count": 432633,
        "treatment_count": 16768,
        "diagnosis_count": 49920,
        "mutation_count": 5135,
        "researchsubject_count": 56604,
        "subject_count": 46551,
    }

    # print(box)
    for i in test_count:
        assert i == test_dict


test_Q_count()
