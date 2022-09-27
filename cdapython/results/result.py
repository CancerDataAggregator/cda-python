"""
result is a convenient wrapper around the response object from the CDA service it adds user functionality.
like creating dataframe and manipulating data for ease-of-use such as paginating automatically for the user through their result objects.
"""
import json
import re
from collections import ChainMap
from io import StringIO
from multiprocessing.pool import ApplyResult
from time import sleep
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    Iterator,
    List,
    Optional,
    Pattern,
    Type,
    Union,
)

from cda_client.api.query_api import QueryApi
from cda_client.model.query_response_data import QueryResponseData
from pandas import DataFrame, Series, json_normalize, read_csv, MultiIndex
from rich import print
from rich.table import Table
from typing_extensions import Literal

from cdapython.Paginator import Paginator
from cdapython.results.base import BaseResult
from cdapython.utils.state import State


class _QEncoder(json.JSONEncoder):
    """_QEncoder this is a a class to help with json conversion
        the standard json dump

    Args:
        json (_type_): _description_
    """

    def decode(self, object_json) -> str:
        """
        This is for json decoding super method
        """
        regex: Pattern[str] = re.compile(r"([^\"\\]|\\([\"\\\/bfnrt]|u[a-zA-Z\d]{4}))+")

        if isinstance(object_json, str):
            print(regex.match(object_json, pos=0))
        return object_json


class Result(BaseResult):
    """
    The Results Class is a convenient wrapper around the response object from the CDA service.
    """

    def __init__(
        self,
        api_response: QueryResponseData,
        query_id: str,
        offset: Optional[int],
        limit: Optional[int],
        api_instance: QueryApi,
        show_sql: bool,
        show_count: bool,
        format_type: str = "json",
    ) -> None:
        super().__init__(show_sql, show_count, format_type)
        self._api_response: QueryResponseData = api_response
        self._result: List[Any] = self._api_response.result
        self._query_id: str = query_id
        self._offset: Optional[int] = offset
        self._limit: Optional[int] = limit
        self._api_instance: QueryApi = api_instance
        self._df: DataFrame

        if self.format_type == "tsv" and isinstance(self._result, list):
            data_text: str = ""
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
        if isinstance(self._offset, int) and isinstance(self._limit, int):
            return (self._offset + self._limit) <= self.total_row_count
        return False

    def paginator(
        self,
        output: str = "",
        to_df: bool = False,
        to_list: bool = False,
        page_size: int = None,
    ) -> Paginator:
        """_summary_
        paginator this will automatically page over results
        Args:
            to_df (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        if page_size is None and isinstance(self._limit, int):
            page_size = self._limit

        return Paginator(
            self,
            to_df=to_df,
            to_list=to_list,
            limit=page_size,
            output=output,
            format_type=self.format_type,
        )

    def auto_paginator(
        self,
        output: str = "",
        to_df: bool = False,
        to_list: bool = False,
        page_size: Union[int, None] = None,
    ) -> Union[DataFrame, List[Any]]:
        """
        auto_paginator is a method that will loop for you

        Args:
            output (str, optional): _description_. Defaults to "".
            to_df (bool, optional): _description_. Defaults to False.
            to_list (bool, optional): _description_. Defaults to False.
            limit (Union[int, None], optional): _description_. Defaults to None.

        Returns:
            Union[DataFrame, List[Any]]: _description_
        """
        if page_size is None and isinstance(self._limit, int):
            page_size = self._limit

        iterator: Paginator = Paginator(
            self,
            to_df=to_df,
            to_list=to_list,
            limit=page_size,
            output=output,
            format_type=self.format_type,
        )
        state: State = State(df=DataFrame(), list_array=[])
        for i in iterator:
            if to_df or output == "full_df":
                state.concat_df(i)
            if to_list or output == "full_list":
                state.concat_list(i)
        if to_df or output == "full_df":
            return state.get_df()
        if to_list or output == "full_list":
            return state.get_list()
        return None

    async def async_next_page(
        self,
        limit: Optional[int] = None,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Optional["Result"]:
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
    ) -> Optional["Result"]:
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
    ) -> Optional["Result"]:
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
        return None

    def prev_page(
        self,
        limit: Optional[int] = None,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Optional["Result"]:
        """prev_page


        Returns:
            _type_: _description_
        """
        if isinstance(self._offset, int) and isinstance(self._limit, int):
            _offset: int = self._offset - self._limit
            _offset: int = max(0, _offset)
            _limit: int = limit or self._limit
            return self._get_result(_offset, _limit, async_req, pre_stream)
        return None

    def _get_result(
        self,
        _offset: Optional[int],
        _limit: Optional[int],
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Optional["Result"]:
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
    clz: Type,
    api_instance: QueryApi,
    query_id: str,
    offset: Optional[int],
    limit: Optional[int],
    async_req: Optional[bool],
    pre_stream: bool = True,
    show_sql: bool = False,
    show_count: bool = True,
    format_type: str = "json",
) -> Optional[Result]:
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
