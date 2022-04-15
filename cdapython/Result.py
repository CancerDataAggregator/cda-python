import asyncio
from multiprocessing.pool import ApplyResult
from typing import Counter, List, Union, Dict, Optional
from time import sleep
import json
from cda_client.model.query_response_data import QueryResponseData
from cda_client.api.query_api import QueryApi
from pandas import DataFrame, json_normalize

from cdapython.Paginator import Paginator


class Result:
    """A convenient wrapper around the response object from the CDA service."""

    def __init__(
        self,
        api_response: QueryResponseData,
        query_id: str,
        offset: Optional[int],
        limit: Optional[int],
        api_instance: QueryApi,
        show_sql: bool,
        show_count: bool,
    ) -> None:
        self._api_response = api_response
        self._query_id = query_id
        self._offset = offset
        self._limit = limit
        self._api_instance = api_instance
        self.show_sql: bool = show_sql
        self._dataTmp: List = []
        self.show_count = show_count
        # add a if check to query output for counts to hide sql

    def __repr_value(self, show_value: bool, show_count: bool):
        return f"""
            QueryID: {self._query_id}
            {"Query:"+self.sql if show_value is True else ""  }
            Offset: {self._offset}
            Count: {self.count}
            Total Row Count: {self.total_row_count}
            More pages: {self.has_next_page}
            """

    def __repr__(self) -> str:
        return self.__repr_value(show_value=self.show_sql, show_count=self.show_count)

    def __str__(self) -> str:
        return self.__repr_value(show_value=self.show_sql, show_count=self.show_count)

    def __dict__(self):
        return {key: value for (key, value) in self._api_response.results}

    # def __flatten_json(self, obj):
    #     ret = {}

    #     def flatten(x, flatten_key=""):
    #         if isinstance(x, dict):
    #             for current_key in x:
    #                 flatten(x[current_key], flatten_key + current_key + "_")
    #         elif isinstance(x, list):
    #             for index, elem in enumerate(x):
    #                 flatten(elem, flatten_key + str(index) + "_")
    #         else:
    #             ret[flatten_key[:-1]] = x

    #     flatten(obj)
    #     return ret

    def __contains__(self, value):
        exist = False
        for item in self._api_response.result:
            if value in item.values():
                exist = True

        return exist

    @property
    def sql(self) -> str:
        return self._api_response.query_sql

    @property
    def count(self) -> int:
        return len(self._api_response.result)

    @property
    def total_row_count(self) -> int:
        return self._api_response.total_row_count

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
    ) -> Optional[DataFrame]:
        """[summary]
        Creates a pandas DataFrame for the Results

        Returns:
            DataFrame: [description]
        """
        if record_path is None:
            return json_normalize(self.__iter__())

        return json_normalize(
            self.__iter__(), record_path=record_path, meta=meta, meta_prefix=meta_prefix
        )

    def __len__(self):
        return self.count

    def paginator(self, to_df: bool = False):
        return Paginator(self, to_df=to_df)

    def __getitem__(
        self, idx: Union[int, slice]
    ) -> Union[Dict[str, Optional[str]], List[dict]]:
        if isinstance(idx, int):
            if idx < 0:
                idx = self.count + idx
            return self._api_response.result[idx]
        else:
            # for slicing result
            start, stop, step = idx.indices(self.count)
            range_index = range(start, stop, step)
            return [self._api_response.result[i] for i in range_index]

    def __iter__(self):
        return iter(self._api_response.result)

    def pretty_print(self, idx: Optional[int] = None):
        if idx is None:
            for i in range(self.count):
                print(json.dumps(self[i], indent=4))
        else:
            print(json.dumps(self[idx], indent=4))

    async def async_next_page(
        self, limit: Optional[int] = None, async_req=False, pre_stream=True
    ):
        return self.next_page()

    async def async_prev_page(
        self, limit: Optional[int] = None, async_req=False, pre_stream=True
    ):
        return self.prev_page()

    def next_page(self, limit: Optional[int] = None, async_req=False, pre_stream=True):
        if not self.has_next_page:
            raise StopIteration
        if isinstance(self._offset, int) and isinstance(self._limit, int):
            _offset = self._offset + self._limit
            _limit = limit or self._limit
            return self._get_result(_offset, _limit, async_req, pre_stream)

    def prev_page(self, limit=None, async_req=False, pre_stream=True):
        _offset = self._offset - self._limit
        _offset = max(0, _offset)
        _limit = limit or self._limit
        return self._get_result(_offset, _limit, async_req, pre_stream)

    def _get_result(self, _offset: int, _limit: int, async_req=False, pre_stream=True):
        return get_query_result(
            self._api_instance, self._query_id, _offset, _limit, async_req, pre_stream
        )


def get_query_result(
    api_instance: QueryApi,
    query_id: str,
    offset: int,
    limit: int,
    async_req: bool,
    pre_stream: bool = True,
    show_sql: bool = True,
    show_count: bool = True,
) -> Optional[Result]:
    """[summary]
        This will call the next query and wait for the result then return a Result object to the user.
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
        )

        if isinstance(response, ApplyResult):
            response = response.get()
            # for chunk in response.stream(32):
            #     print(bytes(chunk).decode("utf-8"))

        sleep(2.5)
        if response.total_row_count is not None:
            return Result(
                response, query_id, offset, limit, api_instance, show_sql, show_count
            )
