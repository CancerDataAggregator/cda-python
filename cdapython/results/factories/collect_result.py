from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, List, Union

from cda_client.api.query_api import QueryApi
from cda_client.model.query_response_data import QueryResponseData

from cdapython.results.factories.not_paginated_result import NotPaginatedResult
from cdapython.results.factories.result_factory import AbstractFactory
from cdapython.utils.none_check import none_check

if TYPE_CHECKING:
    from cdapython.results.result import Result


class CollectResult(NotPaginatedResult):
    """_summary_
    This is made for Collecti
    Args:
        NotPaginatedResult (_type_): _description_
    """

    def __init__(
        self,
        api_response: QueryResponseData,
        query_id: str,
        offset: int,
        limit: int,
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
            format_type=format_type,
        )

    def extend_result(self, result: Result) -> None:
        """_summary_
        This will method will
        Args:
            result (Result): _description_
        """
        if none_check(self._result):
            self._result.extend(result.to_list())

    def get_all(
        self,
        output: str = "",
        page_size: Union[None, int] = None,
        show_bar: bool = True,
    ) -> Result:
        """
        This will page
        Args:
            output (str, optional): _description_. Defaults to "".
            page_size (Union[None, int], optional): _description_. Defaults to None.
            show_bar (bool, optional): _description_. Defaults to True.

        Returns:
            Result: _description_
        """
        return super().get_all(output, page_size, show_bar)

    def paginator(
        self,
        output: str = "",
        to_df: bool = False,
        to_list: bool = False,
        page_size: int = None,
        show_bar: bool = False,
    ):
        return super().paginator(output, to_df, to_list, page_size, show_bar)

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: Result) -> CollectResult:
            return CollectResult(
                api_response=q_object._api_response,
                query_id=q_object._query_id,
                offset=q_object._offset,
                limit=q_object._limit,
                api_instance=q_object._api_instance,
                show_sql=q_object.show_sql,
                show_count=q_object.show_count,
                format_type="json",
                result=q_object._result,
            )
