"""
result is a convenient wrapper around the response object
from the CDA service it adds user functionality.
like creating dataframe and manipulating data for ease-of-use such
as paginating automatically for the user through their result objects.
"""

from __future__ import annotations

from collections import ChainMap
from io import StringIO
from multiprocessing.pool import ApplyResult
from time import sleep
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union, cast

from cda_client.api.query_api import QueryApi
from cda_client.model.query_response_data import QueryResponseData
from pandas import DataFrame, read_csv
from typing_extensions import Literal, Self

from cdapython.Paginator import Paginator
from cdapython.results import COLLECT_RESULT
from cdapython.results.base import BaseResult
from cdapython.results.factories.result_factory import ResultFactory

if TYPE_CHECKING:
    from cdapython.results import CollectResult
    from cdapython.results.columns_result import ColumnsResult
    from cdapython.results.string_result import StringResult

_T = TypeVar("_T")


class Result(BaseResult):
    """
    The Results Class is a convenient wrapper around the
    response object from the CDA service.
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
        format_type: str = "json",
    ) -> None:
        self._api_response: QueryResponseData = api_response
        self._result: List[Any] = self._api_response.result
        self._query_id: str = query_id
        self._offset: int = offset
        self._limit: int = limit
        self._api_instance: QueryApi = api_instance
        self._df: DataFrame
        super().__init__(
            show_sql=show_sql,
            show_count=show_count,
            format_type=format_type,
            result=self._api_response.result,
        )

        if self.format_type == "tsv" and isinstance(self._result, list):
            data_text: str = "\n".join(
                map(lambda e: str(e).replace("\n", ""), self._result)
            )
            self._df = read_csv(StringIO(data_text), sep="\t")

        # add a if check to query output for counts to hide sql

    def _repr_value(self, show_value: Optional[bool]) -> str:
        return f"""
            {"Query:"+self.sql if show_value is True else ""  }
            Offset: {self._offset}
            Count: {self.count}
            Total Row Count: {self.total_row_count}
            More pages: {self.has_next_page}
            """

    def __repr__(self) -> str:
        return self._repr_value(show_value=self.show_sql)

    def __str__(self) -> str:
        return self._repr_value(show_value=self.show_sql)

    def __dict__(self) -> Dict[str, Any]:  # type: ignore
        return dict(ChainMap(*self._result))

    def __eq__(self, __other: object) -> Union[Any, Literal[False]]:
        return isinstance(__other, Result) and self._result == __other._result

    def __hash__(self) -> int:
        return hash(tuple(self._result))

    def __contains__(self, value: str) -> bool:
        exist: bool = False
        for item in self._result:
            if value in item.values():
                exist = True

        return exist

    @property
    def sql(self) -> str:
        """
        Return the results sql back in a property

        Returns:
            str: sql query
        """
        return str(self._api_response.query_sql)

    @property
    def count(self) -> int:
        """
        gets the count of the current list of results
        Returns:
            int
        """
        return len(self._result)

    @property
    def total_row_count(self) -> int:
        """
        get the total count for the query

        Returns:
            int: _description_
        """
        return int(self._api_response.total_row_count)

    @property
    def has_next_page(self) -> bool:
        """This checks to see if there is a next page

        Returns:
            bool: returns a bool value if there is a next page
        """
        return (self._offset + self._limit) < self.total_row_count

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

        page_size = page_size if page_size != 0 else self._limit

        return Paginator(
            self,
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
            page_size = self._limit

        iterator: Paginator = Paginator(
            self,
            to_df=False,
            to_list=False,
            limit=page_size,
            output=output,
            format_type=self.format_type,
            show_bar=show_bar,
        )
        # add this to cast to a subclass of CollectResult
        collect_result: "CollectResult" = cast(
            "CollectResult", ResultFactory.create_entity(COLLECT_RESULT, self)
        )

        for index, i in enumerate(iterator):
            if index == 0:
                continue
            if isinstance(i, Result):
                collect_result.extend_result(i)

        return collect_result

    async def async_next_page(
        self,
        limit: Optional[int] = None,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Union[Result, StringResult, ColumnsResult, None]:
        """async wrapper for next page

        Returns:
            _type_: _description_
        """
        return self.next_page(limit=limit, async_req=async_req, pre_stream=pre_stream)

    async def async_prev_page(
        self,
        limit: Optional[int] = None,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Union[Result, StringResult, ColumnsResult, None]:
        """
        async wrapper for prev page

        Returns:
            _type_: _description_
        """

        return self.prev_page(limit=limit, async_req=async_req, pre_stream=pre_stream)

    def next_page(
        self,
        limit: Optional[int] = None,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Union[Result, StringResult, ColumnsResult, None]:
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
        if isinstance(self._offset, int) and isinstance(self._limit, int):
            _offset: int = self._offset + self._limit
            _limit: int = limit or self._limit
            return self._get_result(_offset, _limit, async_req, pre_stream)

    def prev_page(
        self,
        limit: Optional[int] = None,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Union[Result, StringResult, ColumnsResult, None]:
        """prev_page


        Returns:
            _type_: _description_
        """
        if isinstance(self._offset, int) and isinstance(self._limit, int):
            offset = self._offset - self._limit
            offset = max(0, offset)
            limit = limit or self._limit
            return self._get_result(offset, limit, async_req, pre_stream)

    def _get_result(
        self,
        _offset: int,
        _limit: int,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Union[Result, StringResult, ColumnsResult, None]:
        return get_query_result(
            self.__class__,
            self._api_instance,
            self._query_id,
            _offset,
            _limit,
            async_req,
            pre_stream,
            format_type=self.format_type,
        )


def get_query_result(
    clz,
    api_instance: QueryApi,
    query_id: str,
    offset: Optional[int],
    limit: Optional[int],
    async_req: Optional[bool],
    pre_stream: bool = True,
    show_sql: bool = False,
    show_count: bool = True,
    format_type: str = "json",
) -> Union[Result, StringResult, ColumnsResult, None]:
    """
        This will call the next query and wait for the result \
        then return a Result object to the user.
    Args:
        api_instance (QueryApi): [description]
        query_id (str): [description]
        offset (int): [description]
        limit (int): [description]
        async_req (bool): [description]
        pre_stream (bool, optional): [description]. Defaults to True.

    Returns:
        Optional[Result]: [returns a class Result Object]
    """
    while True:
        response = api_instance.query(
            id=query_id,
            offset=offset,
            limit=limit,
            async_req=async_req,
            _preload_content=pre_stream,
            _check_return_type=False,
        )

        if isinstance(response, ApplyResult):
            response = response.get()

        sleep(2.5)
        if response.total_row_count is not None:
            return clz(
                response,
                query_id,
                offset,
                limit,
                api_instance,
                show_sql,
                show_count,
                format_type,
            )
