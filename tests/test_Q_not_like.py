from unittest import TestCase
from tests.global_settings import host, table
from cdapython.results.count_result import CountResult
from unittest.mock import patch
from pandas import DataFrame
from tests.fake_result import FakeResultData

result = [
    {
        "total": 98467,
        "files": 38226418,
        "system": [
            {"system": "GDC", "count": 45882},
            {"system": "IDC", "count": 58584},
            {"system": "PDC", "count": 1343},
        ],
        "sex": [
            {"sex": "not reported", "count": 266},
            {"sex": "female", "count": 45574},
            {"sex": None, "count": 52541},
            {"sex": "unspecified", "count": 5},
            {"sex": "unknown", "count": 81},
        ],
        "race": [
            {"race": None, "count": 52541},
            {"race": "white", "count": 25720},
            {"race": "asian", "count": 1606},
            {"race": "not reported", "count": 12204},
            {"race": "chinese", "count": 25},
            {"race": "black or african american", "count": 2761},
            {"race": "Unknown", "count": 2033},
            {"race": "other", "count": 532},
            {"race": "not allowed to collect", "count": 955},
            {"race": "native hawaiian or other pacific islander", "count": 29},
            {"race": "american indian or alaska native", "count": 60},
            {"race": "unknown", "count": 1},
        ],
        "ethnicity": [
            {"ethnicity": "not hispanic or latino", "count": 25417},
            {"ethnicity": "not reported", "count": 14530},
            {"ethnicity": None, "count": 52541},
            {"ethnicity": "hispanic or latino", "count": 1685},
            {"ethnicity": "Unknown", "count": 2223},
            {"ethnicity": "not allowed to collect", "count": 2069},
            {"ethnicity": "unknown", "count": 2},
        ],
        "cause_of_death": [
            {"cause_of_death": None, "count": 97606},
            {"cause_of_death": "Not Reported", "count": 573},
            {"cause_of_death": "HCC recurrence", "count": 2},
            {"cause_of_death": "Cancer Related", "count": 138},
            {"cause_of_death": "Unknown", "count": 109},
            {"cause_of_death": "Infection", "count": 4},
            {"cause_of_death": "Not Cancer Related", "count": 31},
            {"cause_of_death": "Cancer cell proliferation", "count": 1},
            {"cause_of_death": "Metastasis", "count": 1},
            {"cause_of_death": "Surgical Complications", "count": 1},
            {"cause_of_death": "Cardiovascular Disorder, NOS", "count": 1},
        ],
    }
]

fake: FakeResultData = FakeResultData(result)
fake_result: CountResult = CountResult(
    api_response=fake.api_response,
    query_id=fake.query_id,
    offset=fake.offset,
    limit=fake.limit,
    api_instance=fake.api_instance,
    show_sql=fake.show_sql,
    show_count=fake.show_count,
    format_type=fake.format_type,
)


class TestData(TestCase):
    @patch("cdapython.Q")
    def test_not_like(self, data) -> None:
        q = (
            data('sex NOT LIKE "m%"')
            .subject.count.run(host=host, table=table)
            .return_value
        ) = fake_result
        print(q.to_list())
        assert isinstance(q.to_list(), list) is True
        assert isinstance(q.to_dataframe(), DataFrame) is True
