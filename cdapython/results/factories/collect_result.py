from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Union

from cda_client.api.query_api import QueryApi
from cda_client.model.query_response_data import QueryResponseData

from cdapython.results.factories.not_paginated_result import NotPaginatedResult
from cdapython.results.factories.result_factory import AbstractFactory
from cdapython.utils.none_check import none_check

if TYPE_CHECKING:
    from cdapython.results.result import Result


class CollectResult(NotPaginatedResult):
    def __init__(
        self,
        api_response: QueryResponseData,
        query_id: str,
        offset: Union[int, None],
        limit: Union[int, None],
        api_instance: QueryApi,
        show_sql: bool,
        show_count: bool,
        result: List[Any],
        format_type: str = "json",
    ) -> None:
        self._result = result
        super().__init__(
            api_response=api_response,
            query_id=query_id,
            offset=offset,
            limit=limit,
            api_instance=api_instance,
            show_sql=show_sql,
            show_count=show_count,
            format_type="json",
        )

    def extend_result(self, result:Result) -> None:
        if none_check(self._result):
            self._result.extend(result.to_list())

    class Factory(AbstractFactory):
        @staticmethod
        def create(result_object: Result) -> CollectResult:
            return CollectResult(
                api_response=result_object._api_response,
                query_id=result_object._query_id,
                offset=result_object._offset,
                limit=result_object._limit,
                api_instance=result_object._api_instance,
                show_sql=result_object.show_sql,
                show_count=result_object.show_count,
                format_type="json",
                result=result_object._result,
            )
