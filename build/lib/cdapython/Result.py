import json
from collections import ChainMap
from multiprocessing.pool import ApplyResult
from multiprocessing.pool import ApplyResult
from typing import ChainMap, Counter, List, Union, Dict, Optional
from time import sleep
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from cda_client.api.query_api import QueryApi
from cda_client.model.query_response_data import QueryResponseData
from pandas import DataFrame, json_normalize, read_csv
from io import StringIO
from cdapython.Paginator import Paginator
from rich import print

if TYPE_CHECKING:
    from cdapython.Q import Q


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
        Q_object: Optional["Q"] = None,
    ) -> None:
        self._api_response: QueryResponseData = api_response
        self.__result = self._api_response.result
        self._query_id: Optional[str] = query_id
        self._offset: Optional[int] = offset
        self._limit: Optional[int] = limit
        self._api_instance: QueryApi = api_instance
        self.show_sql: Optional[bool] = show_sql
        self.show_count: Optional[bool] = show_count
        self.format_type = format_type
        self._df: DataFrame
        self.Q_object: "Q" = Q_object

        if self.format_type == "tsv" and isinstance(self._api_response.result, list):
            data_text: str = ""
            data_text = "\n".join(
                map(lambda e: e.replace("\n", ""), self._api_response.result)
            )
            self._df = read_csv(StringIO(data_text), sep="\t")

        # add a if check to query output for counts to hide sql

    def __repr_value(
        self, show_value: Optional[bool], show_count: Optional[bool]
    ) -> str:
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

    def __dict__(self) -> Dict[str, Any]:
        return dict(ChainMap(*self.__result))

    def __eq__(self, __other: object):
        return (
            isinstance(__other, Result)
            and self._api_response.result == __other._api_response.result
        )

    def __ne__(self, __o: object) -> bool:
        result = self.__eq__(__o)

        if result is NotImplemented:
            return NotImplemented
        else:
            return not result

    def __hash__(self):
        return hash(tuple(self._api_response.result))

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

    def __contains__(self, value: str):
        exist = False
        for item in self.__result:
            if value in item.values():
                exist = True

        return exist

    @property
    def sql(self) -> str:
        return self._api_response.query_sql

    @property
    def count(self) -> int:
        return len(self.__result)

    @property
    def total_row_count(self) -> int:
        return self._api_response.total_row_count

    @property
    def has_next_page(self) -> bool:
        if isinstance(self._offset, int) and isinstance(self._limit, int):
            return (self._offset + self._limit) <= self.total_row_count
        return False

    def counts(self):
        """calls Q counts

        Returns:
            _type_: _description_
        """
        return self.Q_object.counts(
            host=self.Q_object._CURRENT_HOST,
            version=self.Q_object._CURRENT_TABLE_VERSION,
        )

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
        if self.format_type == "tsv":
            return self._df

        if record_path is None:
            return json_normalize(self.__iter__())

        return json_normalize(
            self.__iter__(), record_path=record_path, meta=meta, meta_prefix=meta_prefix
        )

    def to_list(self) -> list:
        """_summary_

        Returns:
            list: _description_
        """
        return self._api_response.result

    def to_dict(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        return dict(ChainMap(*self._api_response.result))

    def __len__(self):
        return self.count

    def paginator(self, to_df: bool = False):
        """_summary_
        paginator this will automatically page over results
        Args:
            to_df (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        return Paginator(self, to_df=to_df, format_type=self.format_type)

    def __getitem__(
        self, idx: Union[int, slice]
    ) -> Union[Dict[str, Optional[str]], List[Dict[Any, Any]]]:

        if isinstance(self._api_response.result, DataFrame):
            return self._api_response.result.loc[idx]

        if isinstance(idx, int):
            if idx < 0:
                idx = self.count + idx
            return self.__result[idx]
        else:
            # for slicing result
            start, stop, step = idx.indices(self.count)
            range_index = range(start, stop, step)
            return [self.__result[i] for i in range_index]

    def __iter__(self):
        return iter(self.__result)

    def __aiter__(self):
        async def tmp():
            yield self.__result

        return tmp()

    def pretty_print(self, idx: Optional[int] = None):
        """_summary_
        pretty_print will print out a json object if you pass a index then i will print the object at that index without the index
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
        self, limit: Optional[int] = None, async_req=False, pre_stream=True
    ):
        return self.next_page()

    async def async_prev_page(
        self, limit: Optional[int] = None, async_req=False, pre_stream=True
    ):
        return self.prev_page()

    def next_page(self, limit: Optional[int] = None, async_req=False, pre_stream=True):
        """_summary_
         The next_page function will call the server for the next page using this limit to determine the next level of page results
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

    def prev_page(self, limit=None, async_req=False, pre_stream=True):
        _offset = self._offset - self._limit
        _offset = max(0, _offset)
        _limit = limit or self._limit
        return self._get_result(_offset, _limit, async_req, pre_stream)

    def _get_result(
        self,
        _offset: Optional[int],
        _limit: Optional[int],
        async_req: Optional[bool] = False,
        pre_stream: Optional[bool] = True,
    ):
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
    query_id: Optional[str],
    offset: Optional[int],
    limit: Optional[int],
    async_req: Optional[bool],
    pre_stream: Optional[bool] = True,
    show_sql: Optional[bool] = True,
    show_count: Optional[bool] = True,
    format_type: str = "json",
    Q_object: Optional["Q"] = None,
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
            _check_return_type=False,
        )

        if isinstance(response, ApplyResult):
            response = response.get()
            # for chunk in response.stream(32):
            #     print(bytes(chunk).decode("utf-8"))

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
                Q_object,
            )
