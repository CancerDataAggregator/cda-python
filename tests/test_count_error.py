import pytest

from cdapython import Q
from tests.global_settings import host

pytest.skip(reason="Count Query times out with 504 error", allow_module_level=True)


# @pytest.mark.skip(reason="")
def test_count():
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.count.run(host=host)
    print(r)
    assert len(r) > 0


def test_file_count():
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.file.count.run(host=host)
    print(r)
    assert len(r) > 0


def test_diagnosis_count():
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.diagnosis.count.run(host=host)
    print(r)
    assert len(r) > 0


def test_mutation_count():
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.mutation.count.run(host=host)
    print(r)
    assert len(r) > 0


def test_researchsubject_count():
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.researchsubject.count.run(host=host)
    print(r)
    assert len(r) > 0


def test_researchsubject_file_count():
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.researchsubject.file.count.run(host=host)
    print(r)
    assert len(r) > 0


def test_specimen_count():
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.specimen.count.run(host=host)
    print(r)
    assert len(r) > 0


def test_specimen_file_count():
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.specimen.file.count.run(host=host)
    print(r)
    assert len(r) > 0


def test_subject_count():
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.subject.count.run(host=host)
    print(r)
    assert len(r) > 0


def test_subject_file_count():
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.subject.file.count.run(host=host)
    print(r)
    assert len(r) > 0


def test_treatment_file_count():
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.treatment.count.run(host=host)
    print(r)
    assert len(r) > 0
