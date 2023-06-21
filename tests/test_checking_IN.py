from unittest import mock

from pandas import DataFrame

from cdapython import Q
from cdapython.results.result import Result
from tests.fake_result import FakeResultData
from tests.global_settings import integration_table, localhost
from tests.patcher import Q_import_path_str

result = [
    {
        "subject_id": "TCGA-FI-A2D5",
        "subject_identifier": [
            {"system": "GDC", "value": "TCGA-FI-A2D5"},
            {"system": "IDC", "value": "TCGA-FI-A2D5"},
        ],
        "species": "homo sapiens",
        "sex": "female",
        "race": "white",
        "ethnicity": "not hispanic or latino",
        "days_to_birth": None,
        "subject_associated_project": ["TCGA-UCEC", "tcga_ucec"],
        "vital_status": "Dead",
        "days_to_death": None,
        "cause_of_death": None,
    },
    {
        "subject_id": "TCGA-EO-A22U",
        "subject_identifier": [
            {"system": "GDC", "value": "TCGA-EO-A22U"},
            {"system": "IDC", "value": "TCGA-EO-A22U"},
        ],
        "species": "homo sapiens",
        "sex": "female",
        "race": "white",
        "ethnicity": "not reported",
        "days_to_birth": None,
        "subject_associated_project": ["TCGA-UCEC", "tcga_ucec"],
        "vital_status": "Alive",
        "days_to_death": None,
        "cause_of_death": None,
    },
    {
        "subject_id": "TCGA-A5-A0G2",
        "subject_identifier": [
            {"system": "GDC", "value": "TCGA-A5-A0G2"},
            {"system": "IDC", "value": "TCGA-A5-A0G2"},
        ],
        "species": "homo sapiens",
        "sex": "female",
        "race": "asian",
        "ethnicity": "not hispanic or latino",
        "days_to_birth": None,
        "subject_associated_project": ["TCGA-UCEC", "tcga_ucec"],
        "vital_status": "Alive",
        "days_to_death": None,
        "cause_of_death": None,
    },
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
def test_checking_test(_):
    q1 = Q('subject_id IN ["TCGA-A5-A0G2", "TCGA-EO-A22U", "TCGA-FI-A2D5"]').AND(
        "NOT race IS NULL"
    )
    print(q1.to_json())
    # assert q1.to_dict()["l"]["node_type"] == "IN"
    r = q1.run(host=localhost, table=integration_table)
    print(r.to_list())
    assert isinstance(r.to_list(), list) is True
    assert isinstance(r.to_dataframe(), DataFrame) is True


test_checking_test()
