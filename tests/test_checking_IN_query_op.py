from unittest import mock
from cdapython import query
from cdapython.results.result import Result

# from tests.global_settings import host, table
from tests.fake_result import FakeResultData

result = [
    {
        "id": "TCGA-E2-A10A",
        "identifier": [
            {"system": "GDC", "value": "TCGA-E2-A10A"},
            {"system": "PDC", "value": "TCGA-E2-A10A"},
            {"system": "IDC", "value": "TCGA-E2-A10A"},
        ],
        "species": "homo sapiens",
        "sex": "female",
        "race": "white",
        "ethnicity": "not hispanic or latino",
        "days_to_birth": -15085,
        "subject_associated_project": ["TCGA-BRCA", "tcga_brca", "CPTAC-TCGA"],
        "vital_status": "Alive",
        "days_to_death": None,
        "cause_of_death": None,
    }
]
fake: FakeResultData = FakeResultData()
fake.result_data = result

results: Result = Result(
    api_response=fake.api_response,
    query_id=fake.query_id,
    offset=fake.offset,
    limit=fake.limit,
    api_instance=fake.api_instance,
    show_sql=fake.show_sql,
    show_count=fake.show_count,
    format_type=fake.format_type,
)


@mock.patch("cdapython.Q.run", return_value=results)
def checking_test(a):
    q1 = query(
        "ResearchSubject.id IN ['4da7abaf-ac7a-41c0-8033-5780a398545c','010df72d-63d9-11e8-bcf1-0a2705229b82']"
    )
    assert q1.query.to_dict()["node_type"] == "IN"
    r = q1.run()
    assert isinstance(r.to_list(), list)
    print(r.to_dataframe()["days_to_birth"])


checking_test()
