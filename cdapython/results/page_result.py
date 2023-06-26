from __future__ import annotations

from multiprocessing.pool import ApplyResult
from typing import TYPE_CHECKING, Any, Coroutine, Union, cast
from urllib.parse import parse_qs, urlparse

import anyio
from cda_client.api.query_api import QueryApi
from cda_client.model.query_response_data import QueryResponseData
from pandas import DataFrame

from cdapython.Paginator import Paginator
from cdapython.results.columns_result import ColumnsResult
from cdapython.results.factories import COLLECT_RESULT
from cdapython.results.factories.collect_result import CollectResult
from cdapython.results.factories.result_factory import ResultFactory
from cdapython.results.result import Result
from cdapython.results.string_result import StringResult

if TYPE_CHECKING:
    from cdapython.Q import Q


class Paged_Result(Result):
    """
    This class is made to hold all of the paged result methods
    """

    def __init__(
        self,
        api_response: QueryResponseData,
        offset: int,
        page_size: int,
        api_instance: QueryApi,
        show_sql: bool,
        show_count: bool,
        q_object: Union[Q, None],
        format_type: str = "json",
    ) -> None:
        self._api_response: QueryResponseData = api_response
        self._result = self._api_response.result
        self._offset: int = offset
        self._page_size: int = page_size
        self._api_instance: QueryApi = api_instance
        self._df: DataFrame
        self.q_object = q_object
        super().__init__(
            api_instance=api_instance,
            api_response=api_response,
            show_sql=show_sql,
            show_count=show_count,
            format_type=format_type,
            offset=offset,
            page_size=page_size,
        )

    def _get_result(
        self,
        _offset: int,
        _limit: int,
        async_req: bool = False,
    ) -> Union[ApplyResult[Any], Paged_Result, Any, None]:
        if self.q_object:
            self.q_object: Q = self.q_object.set_verbose(False)
            return self.q_object.set_config(config=self.q_object.get_config()).run(
                verbose=self.q_object.get_verbose(),
                offset=_offset,
                page_size=_limit,
                async_call=async_req,
                include_total_count=False,
            )
        return None

    def paginator(
        self,
        output: str = "",
        to_df: bool = False,
        to_list: bool = False,
        page_size: int = 0,
        show_bar: bool = False,
    ) -> Paginator:
        """_summary_
        paginator this will automatically page over results
        Args:
            to_df (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """

        page_size = page_size if page_size != 0 else self._page_size

        return Paginator(
            result=self,
            to_df=to_df,
            to_list=to_list,
            limit=page_size,
            output=output,
            format_type=self.format_type,
            show_bar=show_bar,
        )

    def get_all(
        self,
        output: str = "",
        page_size: int = 0,
        show_bar: bool = True,
    ) -> "CollectResult":
        """
        get_all is a method that will loop for you

        Args:
            output (str, optional): _description_. Defaults to "".
            page_size (Union[int, None], optional): _description_. Defaults to None.

        Returns:
            Union[DataFrame, List[Any]]: _description_
        """

        if page_size == 0:
            page_size = self._page_size

        iterator: Paginator = Paginator(
            result=self,
            to_df=False,
            to_list=False,
            limit=page_size,
            output=output,
            format_type=self.format_type,
            show_bar=show_bar,
        )
        # add this to cast to a subclass of CollectResult
        collect_result: "CollectResult" = cast(
            "CollectResult",
            ResultFactory.create_entity(id=COLLECT_RESULT, result_object=self),
        )

        for index, i in enumerate(iterator):
            if index == 0:
                continue
            if isinstance(i, Result):
                collect_result.extend_result(result=i)

        return collect_result

    async def async_next_page(
        self,
        limit: Union[int, None] = None,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Coroutine[Any, Any, Union[ApplyResult[Any], Result, Paged_Result, Any, None]]:
        """async wrapper for next page

        Returns:
            _type_: _description_
        """
        return anyio.to_thread.run_sync(self.next_page, limit, async_req, pre_stream)

    async def async_prev_page(
        self,
        limit: Union[int, None] = None,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Coroutine[
        Any, Any, Union[Result, StringResult, ColumnsResult, Paged_Result, None]
    ]:
        """
        async wrapper for prev page

        Returns:
            _type_: _description_
        """
        return anyio.to_thread.run_sync(self.prev_page, limit, async_req, pre_stream)

    def next_page(
        self,
        limit: Union[int, None] = None,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Union[ApplyResult[Any], Result, Paged_Result, None]:
        """
        The next_page function will call the server for the next page using this \
        limit to determine the next level of page results
        Args:
            limit (Optional[int], optional): _description_. Defaults to None.
            async_req (bool, optional): _description_. Defaults to False.
            pre_stream (bool, optional): _description_. Defaults to True.

        Raises:
            StopIteration: _description_

        Returns:
            _type_: _description_
        """
        if not self.has_next_page:
            raise StopIteration
        if isinstance(self._offset, int) and isinstance(self._page_size, int):
            self._page_size = int(
                parse_qs(urlparse(self._api_response["next_url"]).query)["limit"][0]
            )
            self._offset = int(
                parse_qs(urlparse(self._api_response["next_url"]).query)["offset"][0]
            )

            return self._get_result(_offset=self._offset, _limit=self._page_size)

    def prev_page(
        self,
        limit: Union[int, None] = None,
    ) -> Union[Result, Paged_Result, Any, None]:
        """prev_page


        Returns:
            _type_: _description_
        """
        if isinstance(self._offset, int) and isinstance(self._page_size, int):
            offset = self._offset - self._page_size
            offset = max(0, offset)
            self._page_size = limit or self._page_size
            return self._get_result(offset, self._page_size)


def get_query_result(
    clz: Any,
    api_instance: QueryApi,
    offset: int,
    limit: int,
    q_object: Q,
    async_req: bool = False,
    pre_stream: bool = True,
    show_sql: bool = False,
    show_count: bool = True,
    format_type: str = "json",
) -> Union[Result, StringResult, ColumnsResult, None]:
    """
        This will call the next query and wait for the result
        then return a Result object to the user.
    Args:
        api_instance (QueryApi): [description]
        offset (int): [description]
        limit (int): [description]
        async_req (bool): [description]
        pre_stream (bool, optional): [description]. Defaults to True.

    Returns:
        Optional[Result]: [returns a class Result Object]
    """

    response = q_object._call_endpoint(
        api_instance=api_instance,
        limit=limit,
        offset=offset,
        dry_run=q_object.dry_run,
        async_req=async_req,
    )

    if isinstance(response, ApplyResult):
        response = response.get()

    if response.total_row_count is not None:
        return clz(
            response,
            offset,
            limit,
            api_instance,
            show_sql,
            show_count,
            format_type,
        )
