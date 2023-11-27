from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, List, Union

from cda_client.api.query_api import QueryApi
from cda_client.model.query_response_data import QueryResponseData

from cdapython.Paginator import Paginator
from cdapython.results.factories.not_paginated_result import NotPaginatedResult
from cdapython.results.factories.result_factory import AbstractFactory
from cdapython.utils.none_check import none_check
from cda_client.model.paged_response_data import PagedResponseData

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
        api_response: PagedResponseData,
        offset: int,
        limit: int,
        api_instance: QueryApi,
        show_sql: bool,
        result: List[Any],
        format_type: str = "json",
    ) -> None:
        self._result = result
        super().__init__(
            api_response=api_response,
            offset=offset,
            limit=limit,
            api_instance=api_instance,
            show_sql=show_sql,
            format_type=format_type,
        )

    def extend_result(self, result: Result) -> None:
        """_summary_
        This method will concat the list value to a global list
        Args:
            result (Result): _description_
        """
        self._result.extend(result.to_list())

    def get_all(
        self,
        output: str = "",
        limit: Union[None, int] = None,
        show_bar: bool = True,
    ) -> Result:
        """
        This will page through the query results automatically looping and appending result objects to a List
        for the user.
        Args:
            output (str, optional): if you add this output string "full_list"or"full_df" You will either get a list or a DataFrame. Defaults to "".
            limit (int, optional): this can increase the page size results . Defaults to None.  Known issue: the first page is always 100, even when the size is adjusted.
            show_bar (bool, optional): This will show or hide the progress bar. Defaults to False.

        Returns:
            Result: _description_
        """
        return super().get_all(output, limit, show_bar)

    def paginator(
        self,
        output: str = "",
        to_df: bool = False,
        to_list: bool = False,
        limit: int = None,
        show_bar: bool = False,
    ) -> Paginator:
        """
        This will return a pagination class (Collection) for iteration, such as the for loop.
        By default, the pagination object will return a result class, which is normally what you will get from a `Q.run`
        Args:
            output (str, optional): if you add this output string "full_list"or"full_df" You will either get a list or a DataFrame. Defaults to "".
            to_df (bool, optional): This will return a list from the DataFrame. Defaults to False.
            to_list (bool, optional): This will return a list from the paginator. Defaults to False.
            limit (int, optional): this can change the page size of results . Defaults to results limit.
            show_bar (bool, optional): This will show or hide the progress bar. Defaults to False.

        Returns:
            Paginator: _description_
        """
        return super().paginator(
            output=output,
            to_df=to_df,
            to_list=to_list,
            limit=limit,
            show_bar=show_bar,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: Result) -> CollectResult:
            return CollectResult(
                api_response=q_object._api_response,
                offset=q_object._offset,
                limit=q_object._limit,
                api_instance=q_object._api_instance,
                show_sql=q_object.show_sql,
                format_type="json",
                result=q_object._result,
            )
