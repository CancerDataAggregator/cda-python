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
    Union,
)
from cda_client.api.query_api import QueryApi
from cda_client.model.query_response_data import QueryResponseData
from pandas import DataFrame, Series, json_normalize, read_csv
from rich import print
from typing_extensions import Literal

from cdapython.Paginator import Paginator
from cdapython.utils.state import State


class _QEncoder(json.JSONEncoder):
    """_QEncoder this is a a class to help with json conversion
        the standard json dump

    Args:
        json (_type_): _description_
    """

    def decode(self, o):
        regex = re.compile(r"([^\"\\]|\\([\"\\\/bfnrt]|u[a-zA-Z\d]{4}))+")

        if isinstance(o, str):
            print(regex.match(o, pos=0))
        return o


class Result:
    """_summary_
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
        self._api_response: QueryResponseData = api_response
        self._result: List[Any] = self._api_response.result
        self._query_id: str = query_id
        self._offset: Optional[int] = offset
        self._limit: Optional[int] = limit
        self._api_instance: QueryApi = api_instance
        self.show_sql: Optional[bool] = show_sql
        self.show_count: Optional[bool] = show_count
        self.format_type = format_type
        self._df: DataFrame

        if self.format_type == "tsv" and isinstance(self._result, list):
            data_text: str = ""
            data_text = "\n".join(map(lambda e: str(e).replace("\n", ""), self._result))
            self._df = read_csv(StringIO(data_text), sep="\t")

        # add a if check to query output for counts to hide sql

    def _repr_value(
        self, show_value: Optional[bool], show_count: Optional[bool]
    ) -> str:
        return f"""
            {"Query:"+self.sql if show_value is True else ""  }
            Offset: {self._offset}
            Count: {self.count}
            Total Row Count: {self.total_row_count}
            More pages: {self.has_next_page}
            """

    def __repr__(self) -> str:
        return self._repr_value(show_value=self.show_sql, show_count=self.show_count)

    def __str__(self) -> str:
        return self._repr_value(show_value=self.show_sql, show_count=self.show_count)

    def __dict__(self) -> Dict[str, Any]:  # type: ignore
        return dict(ChainMap(*self._result))

    def __eq__(self, __other: object) -> Union[Any, Literal[False]]:
        return isinstance(__other, Result) and self._result == __other.__result

    def __hash__(self) -> int:
        return hash(tuple(self._result))

    def __contains__(self, value: str) -> bool:
        exist = False
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
            int
        """
        return int(self._api_response.total_row_count)

    @property
    def has_next_page(self) -> bool:
        if isinstance(self._offset, int) and isinstance(self._limit, int):
            return (self._offset + self._limit) <= self.total_row_count
        return False

    def to_dataframe(
        self,
        record_path: Optional[Union[str, list]] = None,
        meta: Optional[Union[str, List[Union[str, List[str]]]]] = None,
        meta_prefix: Optional[str] = None,
        max_level: Optional[int] = None,
    ) -> Optional[DataFrame]:
        """[summary]
        Creates a pandas DataFrame for the Results

        Returns:
            DataFrame: [description]
        """
        if self.format_type == "tsv":
            return self._df

        if record_path is None:
            return json_normalize(iter(self))

        return json_normalize(
            iter(self),
            max_level=max_level,
            record_path=record_path,
            meta=meta,
            meta_prefix=meta_prefix,
        )

    def join_as_str(self, key: str, delimiter: str = ",") -> str:
        if key == "":
            raise KeyError("You need to add a value to join on")
        field_split = key.split(".")

        if len(field_split) == 1:
            return delimiter.join([i[key] for i in self._result])

        def find_field(
            current_field_index: int, field_list: List[Any], data: List[Any]
        ) -> Union[str, Any]:
            my_instance = data[field_list[current_field_index]]

            if current_field_index == len(field_list) - 1:
                return my_instance
            if isinstance(my_instance, dict):
                return find_field(current_field_index + 1, field_list, my_instance)
            if isinstance(my_instance, list):
                return delimiter.join(
                    [
                        find_field(current_field_index + 1, field_list, m)
                        for m in my_instance
                    ]
                )

            raise Exception("you messed up")

        return delimiter.join(
            [
                find_field(current_field_index=0, field_list=field_split, data=result)
                for result in self._result
            ]
        )

    def to_list(self) -> List[Any]:
        """_summary_

        Returns:
            list: _description_
        """

        return self._result

    def __len__(self) -> int:
        return self.count

    def paginator(
        self,
        output: str = "",
        to_df: bool = False,
        to_list: bool = False,
        limit: int = None,
    ) -> Paginator:
        """_summary_
        paginator this will automatically page over results
        Args:
            to_df (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        if limit is None:
            if isinstance(self._limit, int):
                limit = self._limit
        return Paginator(
            self,
            to_df=to_df,
            to_list=to_list,
            limit=limit,
            output=output,
            format_type=self.format_type,
        )

    def auto_paginator(
        self,
        output: str = "",
        to_df: bool = False,
        to_list: bool = False,
        limit: int = None,
        host_list=None,
        host_df=None,
    ):
        iterator = Paginator(
            self,
            to_df=to_df,
            to_list=to_list,
            limit=limit,
            output=output,
            format_type=self.format_type,
        )
        state = State(df=DataFrame(), list=[])
        for i in iterator:
            if to_df or output == "full_df":
                state.concat_df(i)
            if to_list or output == "full_list":
                state.concat_list(i)
        if to_df or output == "full_df":
            return state.get_df()
        else:
            return state.get_list()

    def __getitem__(
        self, idx: Union[int, slice]
    ) -> Union[Series, DataFrame, Any, list]:

        if isinstance(self._result, DataFrame):
            return self._result.loc[idx]

        if isinstance(idx, int):
            if idx < 0:
                idx = self.count + idx
            return self._result[idx]
        else:
            # for slicing result
            start, stop, step = idx.indices(self.count)
            range_index = range(start, stop, step)
            return [self._result[i] for i in range_index]

    def __iter__(self) -> Iterator:
        return iter(self._result)

    def __aiter__(self) -> AsyncGenerator[Any, None]:
        async def tmp() -> AsyncGenerator[Any, None]:
            yield self._result

        return tmp()

    def pretty_print(self, idx: Optional[int] = None) -> None:
        """_summary_
        pretty_print will print out a json object if you pass a index then it will print \
        the object at that index without the index
        it will automatically print alll results in the json object
        Args:
            idx (Optional[int], optional): _description_. Defaults to None.
        """
        if idx is None:
            for i in range(self.count):
                print(json.dumps(self[i], indent=4))
        else:
            print(json.dumps(self[idx], indent=4))

    async def async_next_page(
        self,
        limit: Optional[int] = None,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Optional["Result"]:
        return self.next_page(limit=limit, async_req=async_req, pre_stream=pre_stream)

    async def async_prev_page(
        self,
        limit: Optional[int] = None,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Optional["Result"]:
        return self.prev_page(limit=limit, async_req=async_req, pre_stream=pre_stream)

    def next_page(
        self,
        limit: Optional[int] = None,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Optional["Result"]:
        """_summary_
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
            _offset = self._offset + self._limit
            _limit = limit or self._limit
            return self._get_result(_offset, _limit, async_req, pre_stream)
        return None

    def prev_page(
        self,
        limit: Optional[int] = None,
        async_req: bool = False,
        pre_stream: bool = True,
    ) -> Optional["Result"]:
        if isinstance(self._offset, int) and isinstance(self._limit, int):
            _offset = self._offset - self._limit
            _offset = max(0, _offset)
            _limit = limit or self._limit
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
            self._api_instance,
            self._query_id,
            _offset,
            _limit,
            async_req,
            pre_stream,
            format_type=self.format_type,
        )


def get_query_result(
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
    """[summary]
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
            return Result(
                response,
                query_id,
                offset,
                limit,
                api_instance,
                show_sql,
                show_count,
                format_type,
            )
