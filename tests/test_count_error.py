import pytest

from cdapython import Q
from cdapython.results.count_result import CountResult
from tests.fake_result import FakeResultData
from tests.global_settings import host, localhost
from tests.patcher import Q_import_path_str
from unittest.mock import patch

host = localhost
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
    offset=fake.offset,
    limit=fake.limit,
    api_instance=fake.api_instance,
    show_sql=fake.show_sql,
    show_count=fake.show_count,
    format_type=fake.format_type,
)

# @patch("cdapython.Q",create=True, return_value=fake_result)
# def test_count(_):
#     q1 = Q('sex = "male"')
#     q = q1
#     print(q)
#     r = q.count.run(host=host).to_list()
#     print(r)
#     assert len(r) > 0


@patch(
    Q_import_path_str(method="_call_endpoint"), create=True, return_value=fake_result
)
def test_file_count(_):
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.file.count.run(host=host)
    print(r)
    assert len(r) > 0


# @patch(Q_import_path_str(method="_call_endpoint"), return_value=fake_result)
# def test_diagnosis_count(_):
#     q1 = Q('sex = "male"')
#     q = q1
#     print(q)
#     r = q.diagnosis.count.run(host=host)
#     print(r)
#     assert len(r) > 0

# @patch(Q_import_path_str(method="_call_endpoint"), return_value=fake_result)
# def test_mutation_count(_):
#     q1 = Q('sex = "male"')
#     q = q1
#     print(q)
#     r = q.mutation.count.run(host=host)
#     print(r)
#     assert len(r) > 0

# @patch(Q_import_path_str(method="_call_endpoint"), return_value=fake_result)
# def test_researchsubject_count(_):
#     q1 = Q('sex = "male"')
#     q = q1
#     print(q)
#     r = q.researchsubject.count.run(host=host)
#     print(r)
#     assert len(r) > 0

# @patch(Q_import_path_str(method="_call_endpoint"), return_value=fake_result)
# def test_researchsubject_file_count(_):
#     q1 = Q('sex = "male"')
#     q = q1
#     print(q)
#     r = q.researchsubject.file.count.run(host=host)
#     print(r)
#     assert len(r) > 0

# @patch(Q_import_path_str(method="_call_endpoint"), return_value=fake_result)
# def test_specimen_count(_):
#     q1 = Q('sex = "male"')
#     q = q1
#     print(q)
#     r = q.specimen.count.run(host=host)
#     print(r)
#     assert len(r) > 0

# @patch(Q_import_path_str(method="_call_endpoint"), return_value=fake_result)
# def test_specimen_file_count(_):
#     q1 = Q('sex = "male"')
#     q = q1
#     print(q)
#     r = q.specimen.file.count.run(host=host)
#     print(r)
#     assert len(r) > 0

# @patch(Q_import_path_str(method="_call_endpoint"), return_value=fake_result)
# def test_subject_count(_):
#     q1 = Q('sex = "male"')
#     q = q1
#     print(q)
#     r = q.subject.count.run(host=host)
#     print(r)
#     assert len(r) > 0

# @patch(Q_import_path_str(method="_call_endpoint"), return_value=fake_result)
# def test_subject_file_count(_):
#     q1 = Q('sex = "male"')
#     q = q1
#     print(q)
#     r = q.subject.file.count.run(host=host)
#     print(r)
#     assert len(r) > 0

# @patch(Q_import_path_str(method="_call_endpoint"), return_value=fake_result)
# def test_treatment_file_count(_):
#     q1 = Q('sex = "male"')
#     q = q1
#     print(q)
#     r = q.treatment.count.run(host=host)
#     print(r)
#     assert len(r) > 0
