import pytest
from cdapython import Q
from cdapython.results.count_result import CountResult
from cda_client.model.query_response_data import QueryResponseData
from tests.fake_result import FakeResultData
from tests.global_settings import host
from unittest.mock import patch

from tests.patcher import Q_import_path_str

 
result_count_sex_male = {
    "result": [
        {
            "sex": [{"sex": "male", "count": 1}, {"sex": "Male", "count": 1}],
        
        }
    ],
    "query_sql": "",
}


result_sex_male = {
    "result": [
        {
            "sex": [{"sex": "male"}, {"sex": "Male"}],
        
        }
    ],
    "query_sql": "",
}
fake_result = QueryResponseData(result_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_subject_query(m):
    myquery = Q('sex = "male"')
    result = myquery.subject.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_count_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_subject_count_query(m):
    myquery = Q('sex = "male"')
    result = myquery.subject.count.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_subject_file_query(m):
    myquery = Q('primary_diagnosis_site = "brain"')
    result = myquery.subject.file.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_count_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_subject_file_count_query(m):
    myquery = Q('sex = "male"')
    result = myquery.subject.file.count.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_count_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_treatment_count_query(m):
    myquery = Q('sex = "male"')
    result = myquery.treatment.count.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_treatment_query(m):
    myquery = Q('sex = "male"')
    result = myquery.treatment.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_specimen_query(m):
    myquery = Q('sex = "male"')
    result = myquery.specimen.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_count_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_specimen_count_query(m):
    myquery = Q('sex = "male"')
    result = myquery.specimen.count.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_specimen_file_query(m):
    myquery = Q('sex = "male"')
    result = myquery.specimen.file.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_count_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_specimen_file_count_query(m):
    myquery = Q('sex = "male"')
    result = myquery.specimen.file.count.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_researchsubject_query(m):
    myquery = Q('sex = "male"')
    result = myquery.researchsubject.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_count_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_researchsubject_count_query(m):
    myquery = Q('sex = "male"')
    result = myquery.researchsubject.count.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_researchsubject_file_query(m):
    myquery = Q('sex = "male"')
    result = myquery.researchsubject.file.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_count_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_researchsubject_file_count_query(m):
    myquery = Q('sex = "male"')
    result = myquery.researchsubject.file.count.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


@pytest.mark.skip(reason="Returns 500 error CD-648")
def test_mutation_query():
    myquery = Q('SYMBOL LIKE "TP53%"')
    result = myquery.mutation.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


@pytest.mark.skip(reason="Returns 500 error CD-648")
def test_mutation_count_query():
    myquery = Q('SYMBOL LIKE "TP53%"')
    result = myquery.mutation.count.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_diagnosis_query(m):
    myquery = Q('sex = "male"')
    result = myquery.diagnosis.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

fake_result = QueryResponseData(result_count_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_diagnosis_count_query(m):
    myquery = Q('sex = "male"')
    result = myquery.diagnosis.count.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()



fake_result = QueryResponseData(result_sex_male)

@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_bool_query(m):
    myquery = Q('sex = "male"')
    result = myquery.bool_query.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()


fake_result = QueryResponseData(result_count_sex_male )


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_count_query(m):
    myquery = Q('sex = "male"')
    result = myquery.count.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

result_file_tbi = {
    "result": [
        {
            "file": [{"TBI": "TBI"}]
        
        }
    ],
    "query_sql": "",
}
fake_result = QueryResponseData(result_file_tbi)


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_file_query(m):
    myquery = Q('file_format = "TBI"')
    result = myquery.file.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()

result_file_count_tbi = {
    "result": [
        {
            "file": [{"TBI": "TBI", "count":1}]
        
        }
    ],
    "query_sql": "",
}

fake_result = QueryResponseData(result_file_count_tbi)


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_file_count_query(m):
    myquery = Q('file_format = "TBI"')
    result = myquery.file.count.run(host=host, show_sql=True)
    assert len(result) > 0
    result.to_dataframe()
