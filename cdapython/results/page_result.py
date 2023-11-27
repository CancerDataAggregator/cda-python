from __future__ import annotations

from multiprocessing.pool import ApplyResult
from typing import TYPE_CHECKING, Any, Coroutine, List, Union, cast, Optional
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
from cda_client.model.paged_response_data import PagedResponseData

from cdapython.utils.none_check import none_check

if TYPE_CHECKING:
    from cdapython.Q import Q


class Paged_Result(Result):
    """
    This class is made to hold all of the paged result methods
    """

    def __init__(
        self,
        api_response: PagedResponseData,
        offset: int,
        limit: int,
        api_instance: QueryApi,
        show_sql: bool,
        q_object: Union[Q, None],
        format_type: str = "json",
    ) -> None:
        self._api_response: PagedResponseData = api_response
        self._result = self._api_response.result
        self._offset: int = offset
        self._limit: int = limit
        self._api_instance: QueryApi = api_instance
        self._df: DataFrame
        self.q_object = q_object
        super().__init__(
            api_instance=api_instance,
            api_response=api_response,
            show_sql=show_sql,
            format_type=format_type,
            offset=offset,
            limit=limit,
        )

    def _get_result(
        self,
        _offset: int,
        _limit: int,
        async_req: bool = False,
        include_total_count: bool = False,
        show_counts: bool = False,
    ) -> Union[ApplyResult[Any], Paged_Result, Any, None]:
        if self.q_object:
            self.q_object: Q = self.q_object.set_verbose(False)
            self.q_object: Q = self.q_object.set_counts(show_counts=show_counts)
            return self.q_object.set_config(config=self.q_object.get_config()).run(
                verbose=self.q_object.get_verbose(),
                offset=_offset,
                limit=_limit,
                async_call=async_req,
                include_total_count=include_total_count,
                show_counts=self.q_object.get_counts(),
            )
        return None

    def paginator(
        self,
        output: str = "",
        to_df: bool = False,
        to_list: bool = False,
        limit: int = 0,
        show_bar: bool = False,
        show_counts: Optional[bool] = None,
    ) -> Paginator:
        """_summary_
        paginator this will automatically page over results
        Args:
            to_df (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        if show_counts is None:
            show_counts = self.q_object.get_counts()
        limit = limit if limit != 0 else self._limit

        return Paginator(
            result=self,
            to_df=to_df,
            to_list=to_list,
            limit=limit,
            output=output,
            format_type=self.format_type,
            show_bar=show_bar,
            show_counts=show_counts,
        )

    def return_result(
        self, result, output, to_df, to_list
    ) -> Union[DataFrame, List[Any], Paged_Result, StringResult]:
        """
        This return a Result object and DataFrame
        Returns:
            Union[DataFrame, list, Result]: _description_
        """
        var_output: str = none_check(output)
        if var_output == "full_df":
            return result.to_dataframe()
        if var_output == "full_list":
            return result.to_list()
        if to_df:
            return result.to_dataframe()
        if to_list:
            return result.to_list()

        return result

    def get_all(
        self,
        output: str = "",
        limit: int = 0,
        show_bar: bool = True,
        to_df: bool = False,
        to_list: bool = False,
        show_counts: bool = False,
    ) -> "CollectResult":
        """
        This method will automatically paginate and concatenate results for you.
        Args:
            output (str, optional): _description_. Defaults to "".
            limit (int, optional): _description_. Defaults to 0.
            show_bar (bool, optional): _description_. Defaults to True.
            to_df (bool, optional): _description_. Defaults to False.
            to_list (bool, optional): _description_. Defaults to False.
            show_counts (bool, optional): _description_. Defaults to False.

        Returns:
            CollectResult: _description_
        """

        if limit == 0:
            limit = self._limit

        self._api_response = PagedResponseData(
            result=[], query_sql="", total_row_count=0, next_url=None
        )

        new_page_result = Paged_Result(
            api_response=self._api_response,
            offset=0,
            limit=self._limit,
            api_instance=self._api_instance,
            show_sql=self.show_sql,
            q_object=self.q_object,
        )

        iterator: Paginator = Paginator(
            result=new_page_result,
            to_df=False,
            to_list=False,
            limit=limit,
            output=output,
            format_type=self.format_type,
            show_bar=show_bar,
            show_counts=show_counts,
        )
        # add this to cast to a subclass of CollectResult

        collect_result: "CollectResult" = cast(
            "CollectResult",
            ResultFactory.create_entity(
                id=COLLECT_RESULT, result_object=new_page_result
            ),
        )

        for i in iterator:
            if isinstance(i, Result):
                collect_result.extend_result(result=i)

        return self.return_result(
            result=collect_result, output=output, to_df=to_df, to_list=to_list
        )

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
        self, limit: int = 100, show_counts: Optional[bool] = None
    ) -> Union[ApplyResult[Any], Result, Paged_Result, None]:
        """
        The next_page function will call the server for the next page using this \
        limit to determine the next level of page results
        Args:
            limit (Optional[int], optional): _description_. Defaults to None.

        Raises:
            StopIteration: _description_

        Returns:
            _type_: _description_
        """
        if show_counts is None:
            show_counts = self.q_object.get_counts()
        if isinstance(self._offset, int) and isinstance(self._limit, int):
            if self._api_response["next_url"] is not None:
                self._limit = int(
                    parse_qs(urlparse(self._api_response["next_url"]).query)["limit"][0]
                )
                self._offset = int(
                    parse_qs(urlparse(self._api_response["next_url"]).query)["offset"][
                        0
                    ]
                )
            else:
                self._limit = limit

            next_result = self._get_result(
                _offset=self._offset,
                _limit=self._limit,
                include_total_count=True,
                show_counts=show_counts,
            )

            if next_result.total_row_count is not None:
                self.total_row_count = next_result.total_row_count
                return next_result
            return None

    def prev_page(
        self,
        limit: Union[int, None] = None,
    ) -> Union[Result, Paged_Result, Any, None]:
        """prev_page


        Returns:
            _type_: _description_
        """
        if isinstance(self._offset, int) and isinstance(self._limit, int):
            offset = self._offset - self._limit
            offset = max(0, offset)
            self._limit = limit or self._limit
            return self._get_result(offset, self._limit)


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
    include_total_count=False,
    system: str = "",
    show_counts: bool = False,
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
        include_total_count=include_total_count,
        system=system,
        show_counts=show_counts,
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
