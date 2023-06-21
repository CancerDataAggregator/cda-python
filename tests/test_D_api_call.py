from unittest import mock

from pandas import DataFrame

from cdapython import Q
from cdapython.results.result import Result
from tests.fake_result import FakeResultData
from tests.global_settings import host, project
from tests.patcher import Q_import_path_str

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

fake = FakeResultData(result)
fake_result = Result(
    api_response=fake.api_response,
    offset=fake.offset,
    page_size=fake.limit,
    api_instance=fake.api_instance,
    show_sql=fake.show_sql,
    show_count=fake.show_count,
    format_type=fake.format_type,
)


@mock.patch(Q_import_path_str(method="run"), return_value=fake_result)
def test_call_api(a):
    q = Q('id = "TCGA-E2-A10A"')
    r = q.run(verify=False, host=host, table=project)
    assert isinstance(r.sql, str) is True
    assert isinstance(r.to_list(), list) is True
    assert isinstance(r.to_dataframe(), DataFrame) is True


# test_call_api()
