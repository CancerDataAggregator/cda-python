from enum import Enum
from functools import wraps
from typing import Any, List, Union
from unittest import mock

from cdapython.results.count_result import CountResult
from cdapython.results.result import Result
from cdapython.results.string_result import StringResult
from tests.fake_result import FakeResultData


class Result_Type(Enum):
    Result = "Result"
    CountResult = "CountResult"
    StringResult = "StringResult"


class SuperMock:
    def __init__(self, result: List[Any], result_type: Result_Type) -> None:
        self.result: List[Any] = result
        self.result_type = result_type
        self._data: Union[Result, CountResult, StringResult, None] = None

    def __call__(self, func):
        @wraps(func)
        @mock.patch("cdapython.Q.run", return_value=self._data)
        def _patch(*args, **kwargs):
            fake: FakeResultData = FakeResultData(self.result)

            if self.result_type.Result == "Result":
                self._data = Result(
                    api_response=fake.api_response,
                    offset=fake.offset,
                    page_size=fake.limit,
                    api_instance=fake.api_instance,
                    show_sql=fake.show_sql,
                    show_count=fake.show_count,
                    format_type=fake.format_type,
                )
                if self.result_type.CountResult == "CountResult":
                    self._data = CountResult(
                        api_response=fake.api_response,
                        offset=fake.offset,
                        page_size=fake.limit,
                        api_instance=fake.api_instance,
                        show_sql=fake.show_sql,
                        show_count=fake.show_count,
                        format_type=fake.format_type,
                    )
                return func(*args, **kwargs)

        return _patch
