from unittest import TestCase
from unittest.mock import patch

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
fake: FakeResultData = FakeResultData(result)


fake_result: Result = Result(
    api_response=fake.api_response,
    offset=fake.offset,
    limit=fake.limit,
    api_instance=fake.api_instance,
    show_sql=fake.show_sql,
    format_type=fake.format_type,
)


fake_Q_dict = {
    "node_type": "IN",
    "l": {"node_type": "column", "value": "ResearchSubject.id"},
    "r": {
        "node_type": "unquoted",
        "value": "['4da7abaf-ac7a-41c0-8033-5780a398545c','010df72d-63d9-11e8-bcf1-0a2705229b82']",
    },
}


class TestData(TestCase):
    @patch("cdapython.Q")
    def test_checking(self, data) -> None:
        q1 = data(
            """ResearchSubject.id IN 
            ['4da7abaf-ac7a-41c0-8033-5780a398545c','010df72d-63d9-11e8-bcf1-0a2705229b82']
            """
        ).to_dict.return_value = fake_Q_dict
        assert q1["node_type"] == "IN"

    @patch("cdapython.Q")
    def test_call(self, data):
        r: Result = (
            data(
                "ResearchSubject.id IN ['4da7abaf-ac7a-41c0-8033-5780a398545c','010df72d-63d9-11e8-bcf1-0a2705229b82']"
            )
            .run()
            .return_value
        )
        r = fake_result
        assert isinstance(r.to_list(), list) is True
        print(r.to_dataframe()["days_to_birth"])
