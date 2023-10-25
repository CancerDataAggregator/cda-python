import pytest
from cda_client.model.query_response_data import QueryResponseData
from cdapython import Q
from cdapython.results.count_result import CountResult
from tests.fake_result import FakeResultData
from tests.global_settings import host, localhost
from tests.patcher import Q_import_path_str
from unittest.mock import patch
 

result = {
    "result": [
        {
            "subject_id": 57715,
            "file_id": 1449736,
            "subject_identifier_system": [
                {"subject_identifier_system": "CDS", "count": 15818},
                {"subject_identifier_system": "GDC", "count": 41383},
                {"subject_identifier_system": "IDC", "count": 5901},
                {"subject_identifier_system": "PDC", "count": 1198},
            ],
            "sex": [{"sex": "male", "count": 41383}, {"sex": "Male", "count": 16332}],
            "race": [
                {"race": "american indian or alaska native", "count": 59},
                {"race": "American Indian or Alaska Native", "count": 8},
                {"race": "asian", "count": 1531},
                {"race": "Asian", "count": 121},
                {"race": "black or african american", "count": 1932},
                {"race": "Black or African American", "count": 162},
                {"race": "Chinese", "count": 128},
                {"race": "native hawaiian or other pacific islander", "count": 26},
                {"race": "Native Hawaiian or Other Pacific Islander", "count": 4},
                {"race": "not allowed to collect", "count": 1103},
                {"race": "not reported", "count": 9283},
                {"race": "Not Reported", "count": 41},
                {"race": "other", "count": 529},
                {"race": "Other", "count": 2},
                {"race": "unknown", "count": 111},
                {"race": "Unknown", "count": 2488},
                {"race": "Unknown;Not Reported", "count": 1},
                {"race": "white", "count": 24754},
                {"race": "White", "count": 1111},
                {"race": "White;American Indian or Alaska Native", "count": 1},
                {"race": "White;Black or African American", "count": 2},
                {"race": "White;Native Hawaiian or Other Pacific Islander", "count": 1},
                {"race": "null", "count": 14317},
            ],
            "ethnicity": [
                {"ethnicity": "hispanic or latino", "count": 1742},
                {"ethnicity": "Hispanic or Latino", "count": 116},
                {"ethnicity": "not allowed to collect", "count": 1583},
                {"ethnicity": "Not Allowed to Collect", "count": 2},
                {"ethnicity": "not hispanic or latino", "count": 24023},
                {"ethnicity": "Not Hispanic or Latino", "count": 1324},
                {"ethnicity": "not reported", "count": 11739},
                {"ethnicity": "Not Reported", "count": 78},
                {"ethnicity": "unknown", "count": 24},
                {"ethnicity": "Unknown", "count": 2318},
                {"ethnicity": "null", "count": 14766},
            ],
            "cause_of_death": [
                {"cause_of_death": "Cancer Related", "count": 374},
                {"cause_of_death": "Cardiovascular Disorder, NOS", "count": 4},
                {"cause_of_death": "Cerebral Hemorrhage", "count": 1},
                {"cause_of_death": "HCC recurrence", "count": 5},
                {"cause_of_death": "Infection", "count": 10},
                {"cause_of_death": "Metastasis", "count": 1},
                {"cause_of_death": "Not Cancer Related", "count": 80},
                {"cause_of_death": "Not Reported", "count": 176},
                {"cause_of_death": "Surgical Complications", "count": 3},
                {"cause_of_death": "Toxicity", "count": 2},
                {"cause_of_death": "Unknown", "count": 63},
                {"cause_of_death": "null", "count": 56996},
            ],
        }
    ],
    "query_sql": "WITH flattened_result as (SELECT subject.id AS subject_id, file_subject.file_id AS file_id, subject_identifier.system AS subject_identifier_system, subject.sex AS sex, subject.race AS race, subject.ethnicity AS ethnicity, subject.cause_of_death AS cause_of_death FROM subject AS subject  INNER JOIN file_subject AS file_subject ON subject.id = file_subject.subject_id  INNER JOIN subject_identifier AS subject_identifier ON subject.id = subject_identifier.subject_id WHERE (COALESCE(UPPER(subject.sex), '') = UPPER('male'))), subject_identifier_system_count as (SELECT row_to_json(subq) AS json_subject_identifier_system FROM (select subject_identifier_system as subject_identifier_system, count(distinct subject_id) as count from flattened_result group by subject_identifier_system) as subq), sex_count as (SELECT row_to_json(subq) AS json_sex FROM (select sex as sex, count(distinct subject_id) as count from flattened_result group by sex) as subq), race_count as (SELECT row_to_json(subq) AS json_race FROM (select race as race, count(distinct subject_id) as count from flattened_result group by race) as subq), ethnicity_count as (SELECT row_to_json(subq) AS json_ethnicity FROM (select ethnicity as ethnicity, count(distinct subject_id) as count from flattened_result group by ethnicity) as subq), cause_of_death_count as (SELECT row_to_json(subq) AS json_cause_of_death FROM (select cause_of_death as cause_of_death, count(distinct subject_id) as count from flattened_result group by cause_of_death) as subq)  select (SELECT COUNT(DISTINCT subject_id) from flattened_result) as subject_id, (SELECT COUNT(DISTINCT file_id) from flattened_result) as file_id, (SELECT array_agg(json_subject_identifier_system) from subject_identifier_system_count) as subject_identifier_system, (SELECT array_agg(json_sex) from sex_count) as sex, (SELECT array_agg(json_race) from race_count) as race, (SELECT array_agg(json_ethnicity) from ethnicity_count) as ethnicity, (SELECT array_agg(json_cause_of_death) from cause_of_death_count) as cause_of_death",
}


fake_result = QueryResponseData(result)


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_count(_):
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.count.run(host=host).to_list()
    print(r)
    assert len(r) > 0


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_file_count(m):
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    t = q.file.count
    # m = MagicMock("cda_client.api_client.QueryApi.__call_api")
    m.return_value = fake_result
    r = t.run(host=host)
    print(r)
    m.assert_called_once()
    assert len(r) > 0


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_diagnosis_count(_):
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.diagnosis.count.run(host=host)
    print(r)
    assert len(r) > 0


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_mutation_count(_):
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.mutation.count.run(host=host)
    print(r)
    assert len(r) > 0


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_researchsubject_count(_):
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.researchsubject.count.run(host=host)
    print(r)
    assert len(r) > 0


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_researchsubject_file_count(_):
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.researchsubject.file.count.run(host=host)
    print(r)
    assert len(r) > 0


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_specimen_count(_):
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.specimen.count.run(host=host)
    print(r)
    assert len(r) > 0


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_specimen_file_count(_):
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.specimen.file.count.run(host=host)
    print(r)
    assert len(r) > 0


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_subject_count(_):
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.subject.count.run(host=host)
    print(r)
    assert len(r) > 0


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_subject_file_count(_):
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.subject.file.count.run(host=host)
    print(r)
    assert len(r) > 0


@patch(
    "cda_client.api_client.ApiClient.call_api", create=True, return_value=fake_result
)
def test_treatment_file_count(_):
    q1 = Q('sex = "male"')
    q = q1
    print(q)
    r = q.treatment.count.run(host=host)
    print(r)
    assert len(r) > 0
