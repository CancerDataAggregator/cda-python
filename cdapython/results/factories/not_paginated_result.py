from __future__ import annotations

from typing import Union

from cda_client.api.query_api import QueryApi
from cda_client.model.query_response_data import QueryResponseData

from cdapython.results.result import Result

MESSAGE_NOT_ALLOW = "Pagination Not Allow with this method"


class NotPaginatedResult(Result):
    def __init__(
        self,
        api_response: QueryResponseData,
        query_id: str,
        offset: Union[int, None],
        limit: Union[int, None],
        api_instance: QueryApi,
        show_sql: bool,
        show_count: bool,
        format_type: str = "json",
    ) -> None:
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

    def paginator(
        self,
        output: str = "",
        to_df: bool = False,
        to_list: bool = False,
        to_collect_result: bool = False,
        page_size: int = None,
        show_bar: bool = False,
    ):
        """_summary_
        This Object has already been paginated
        Args:
            output (str, optional): _description_. Defaults to "".
            to_df (bool, optional): _description_. Defaults to False.
            to_list (bool, optional): _description_. Defaults to False.
            to_collect_result (bool, optional): _description_. Defaults to False.
            page_size (int, optional): _description_. Defaults to None.
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
        page_size: Union[int, None] = None,
        show_bar: bool = True,
    ):
        """_summary_
        This Object has already been paginated
        Args:
            output (str, optional): _description_. Defaults to "".
            page_size (Union[int, None], optional): _description_. Defaults to None.
            show_bar (bool, optional): _description_. Defaults to True.

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError(MESSAGE_NOT_ALLOW)
