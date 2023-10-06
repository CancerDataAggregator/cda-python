from __future__ import annotations

from typing import TYPE_CHECKING, Union

from cda_client.api.query_api import QueryApi
from cda_client.model.query_response_data import QueryResponseData

from cdapython.results.result import Result

if TYPE_CHECKING:
    from cdapython.Paginator import Paginator

MESSAGE_NOT_ALLOW = "Pagination Not Allow with this method"


class NotPaginatedResult(Result):
    def __init__(
        self,
        api_response: QueryResponseData,
        offset: int,
        limit: int,
        api_instance: QueryApi,
        show_sql: bool,
        show_count: bool,
        format_type: str = "json",
    ) -> None:
        super().__init__(
            api_response=api_response,
            offset=offset,
            limit=limit,
            api_instance=api_instance,
            show_sql=show_sql,
            show_count=show_count,
            format_type=format_type,
        )

    def paginator(
        self,
        output: str = "",
        to_df: bool = False,
        to_list: bool = False,
        limit: int = None,
        show_bar: bool = False,
    ) -> Paginator:
        """
        This Object will create a Paginator class for Implementation
        Args:
            output (str, optional): _description_. Defaults to "".
            to_df (bool, optional): _description_. Defaults to False.
            to_list (bool, optional): _description_. Defaults to False.
            limit (int, optional): _description_. Defaults to None.
            show_bar (bool, optional): _description_. Defaults to False.

        Raises:
            NotImplementedError: _description_

        Returns:
            Paginator: _description_
        """
        raise NotImplementedError(MESSAGE_NOT_ALLOW)

    def get_all(
        self,
        output: str = "",
        limit: Union[int, None] = None,
        show_bar: bool = True,
    ) -> Result:
        """
        This Object will create a paged value that will be Implemented
        Args:
            output (str, optional): _description_. Defaults to "".
            limit (Union[int, None], optional): _description_. Defaults to None.
            show_bar (bool, optional): _description_. Defaults to True.

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError(MESSAGE_NOT_ALLOW)
