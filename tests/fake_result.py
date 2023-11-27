from cda_client.api.query_api import QueryApi, QueryResponseData
from typing_extensions import Literal


class FakeResultData:
    def __init__(self, result_data=[]) -> None:
        self._result_data = result_data

    @property
    def offset(self) -> Literal[0]:
        return 0

    @property
    def limit(self) -> Literal[100]:
        return 100

    @property
    def result_data(self) -> list:
        return self._result_data

    @property
    def api_response(self) -> QueryResponseData:
        return QueryResponseData(
            result=self.result_data,
            query_sql="SELECT * FROM counts",
            total_row_count=100,
        )

    @property
    def api_instance(self) -> QueryApi:
        return QueryApi()

    @property
    def show_sql(self) -> Literal[False]:
        return False

    @property
    def format_type(self) -> str:
        return "json"

    @result_data.setter
    def result_data(self, list_a: list) -> None:
        self._result_data = list_a
