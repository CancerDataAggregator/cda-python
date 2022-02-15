from multiprocessing.pool import ApplyResult
from typing import Counter, Dict, List, Optional, Union
from cdapython.decorators_cache import lru_cache_timed
from time import sleep
from typing import Dict, Optional
import json
from cda_client.model.query_response_data import QueryResponseData
from cda_client.api.query_api import QueryApi
from pandas import DataFrame, json_normalize


class Result:
    """A convenient wrapper around the response object from the CDA service."""

    def __init__(
        self,
        api_response: QueryResponseData,
        query_id: str,
        offset: Optional[int],
        limit: Optional[int],
        api_instance: QueryApi,
    ) -> None:
        self._api_response = api_response
        self._query_id = query_id
        self._offset = offset
        self._limit = limit
        self._api_instance = api_instance
        self.showCounts = True
        # add a if check to query output for counts to hide sql

    def __str__(self) -> str:
        return f"""
        QueryID: {self._query_id}
        Query: {self.sql}
        Offset: {self._offset}
        Count: {self.count}
        Total Row Count: {self.total_row_count}
        {self.countResult}
        More pages: {self.has_next_page}
        """

    def __repr__(self) -> str:
        return f"""
        QueryID: {self._query_id}
        Query: {self.sql}
        Offset: {self._offset}
        Count: {self.count}
        Total Row Count: {self.total_row_count}
        {self.countResult}
        More pages: {self.has_next_page}
        """

    def __dict__(self):
        return self

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
    def countResult(self) -> str:
        if self._api_response.result is None or len(self._api_response.result) == 0:
            return "No counts could be found"

        if "system" in self._api_response.result[0]:
            self.showCounts = False
            text = ""
            data = self._api_response.result
            for item in data:
                for key, value in item.items():
                    text += f"{key} Count: {value} \n \t"
            return f"Total Database Counts:\n\n\t{text}"

        dic = Counter(
            [
                identifier["system"]
                for patient in self._api_response.result
                for file in patient["File"]
                for identifier in file["identifier"]
            ]
        )
        return f"GDC Count: {dic['GDC']} \n \tPDC Count: {dic['PDC']} \n \tIDC Count: {dic['IDC']}"

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
    def has_next_page(self) -> Optional[bool]:
        if isinstance(self._offset, int) and isinstance(self._limit, int):
            return (self._offset + self._limit) <= self.total_row_count
        return None

    def to_DataFrame(
        self,
        record_path: Optional[Union[str, list]],
        meta: Optional[Union[str, List[Union[str, List[str]]]]],
        meta_prefix: Optional[str],
    ):
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

    def stream(self):
        box = []
        while self.has_next_page:
            box.append(self)
            yield self.next_page()
        return box

    def __len__(self):
        return self.count

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
            rangeIndex = range(start, stop, step)
            return [self._api_response.result[i] for i in rangeIndex]

    def __iter__(self):
        return iter(self._api_response.result)

    def pretty_print(self, idx: Optional[int] = None):
        if idx is None:
            for i in range(self.count):
                print(json.dumps(self[i], indent=4))
        else:
            print(json.dumps(self[idx], indent=4))

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

        sleep(2)
        response = api_instance.query(id=query_id, offset=offset, limit=limit)
        if response.total_row_count is not None:
            return Result(response, query_id, offset, limit, api_instance)
