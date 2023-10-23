import pytest
from cdapython import Q
from tests.global_settings import host

def test_subject_query():
    myquery = Q('sex = "male"')
    result = myquery.subject.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


def test_subject_count_query():
    myquery = Q('sex = "male"')
    result = myquery.subject.count.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


def test_subject_file_query():
    myquery = Q('primary_diagnosis_site = "brain"')
    result = myquery.subject.file.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


def test_subject_file_count_query():
    myquery = Q('sex = "male"')
    result = myquery.subject.file.count.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()



def test_treatment_count_query():
    myquery = Q('sex = "male"')
    result = myquery.treatment.count.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


def test_treatment_query():
    myquery = Q('sex = "male"')
    result = myquery.treatment.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


def test_specimen_query():
    myquery = Q('sex = "male"')
    result = myquery.specimen.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


def test_specimen_count_query():
    myquery = Q('sex = "male"')
    result = myquery.specimen.count.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


def test_specimen_file_query():
    myquery = Q('sex = "male"')
    result = myquery.specimen.file.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

def test_specimen_file_count_query():
    myquery = Q('sex = "male"')
    result = myquery.specimen.file.count.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

def test_researchsubject_query():
    myquery = Q('sex = "male"')
    result = myquery.researchsubject.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

def test_researchsubject_count_query():
    myquery = Q('sex = "male"')
    result = myquery.researchsubject.count.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


def test_researchsubject_file_query():
    myquery = Q('sex = "male"')
    result = myquery.researchsubject.file.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


def test_researchsubject_file_count_query():
    myquery = Q('sex = "male"')
    result = myquery.researchsubject.file.count.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

@pytest.mark.skip(reason="Returns 500 error CD-648")
def test_mutation_query():
    myquery = Q('SYMBOL LIKE "TP53%"')
    result = myquery.mutation.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


@pytest.mark.skip(reason="Returns 500 error CD-648")
def test_mutation_count_query():
    myquery = Q('SYMBOL LIKE "TP53%"')
    result = myquery.mutation.count.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()



def test_diagnosis_query():
    myquery = Q('sex = "male"')
    result = myquery.diagnosis.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()



def test_diagnosis_count_query():
    myquery = Q('sex = "male"')
    result = myquery.diagnosis.count.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()



def test_bool_query():
    myquery = Q('sex = "male"')
    result = myquery.bool_query.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

def test_count_query():
    myquery = Q('sex = "male"')
    result = myquery.count.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

def test_file_query():
    myquery = Q('file_format = "TBI"')
    result = myquery.file.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


def test_file_count_query():
    myquery = Q('file_format = "TBI"')
    result = myquery.file.count.run(host=host,show_sql=True)
    assert len(result) > 0
    result.to_dataframe()
