from typing import Any, Dict, List
from unittest import mock

from cdapython import unique_terms
from cdapython.results.result import Result
from tests.fake_result import FakeResultData
from tests.global_settings import host, project

result: List[Dict[str, str]] = [
    {"sex": "null"},
    {"sex": "F"},
    {"sex": "Female"},
    {"sex": "M"},
    {"sex": "Male"},
    {"sex": "Unspecified"},
    {"sex": "female"},
    {"sex": "male"},
    {"sex": "not reported"},
    {"sex": "unknown"},
    {"sex": "unspecified"},
]

fake = FakeResultData(result)
fake_result = Result(
    api_response=fake.api_response,
    offset=fake.offset,
    limit=fake.limit,
    api_instance=fake.api_instance,
    show_sql=fake.show_sql,
    show_count=fake.show_count,
    format_type=fake.format_type,
)


@mock.patch("cdapython.unique_terms", return_value=fake_result)
def test_unique_terms_get_all(_: Any) -> None:
    terms_list = unique_terms("sex").get_all().to_list()
    assert len(terms_list) != 0
