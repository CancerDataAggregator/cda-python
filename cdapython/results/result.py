"""
result is a convenient wrapper around the response object
from the CDA service it adds user functionality.
like creating dataframe and manipulating data for ease-of-use such
as paginating automatically for the user through their result objects.
"""

from __future__ import annotations

from collections import ChainMap
from io import StringIO
from typing import Any, Dict, List, Optional, TypedDict, Union

from cda_client.api.query_api import QueryApi
from cda_client.model.query_response_data import QueryResponseData
from pandas import DataFrame, read_csv
from typing_extensions import Literal

from cdapython.results.base import BaseResult
from cda_client.model.paged_response_data import PagedResponseData


class ResultTypes(TypedDict):
    """
    Type hit for Results
    :param TypedDict: _description_
    :type TypedDict: _type_
    """

    subject_id: Union[str, None]
    species: Union[str, None]
    sex: Union[str, None]
    race: Union[str, None]
    ethnicity: Union[str, None]
    days_to_birth: Union[str, None]
    vital_status: Union[str, None]
    days_to_death: Union[str, None]
    cause_of_death: Union[str, None]
    subject_identifier: Union[Dict[str, Any], None]
    subject_associated_project: Union[List[str], None]


class Result(BaseResult):
    """
    The Results Class is a convenient wrapper around the
    response object from the CDA service.
    """

    def __init__(
        self,
        api_response: PagedResponseData,
        offset: int,
        limit: int,
        api_instance: QueryApi,
        show_sql: bool,
        show_count: bool,
        format_type: str = "json",
    ) -> None:
        self._api_response: PagedResponseData = api_response
        self._result: List[ResultTypes] = self._api_response.result
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
        if self._api_response.total_row_count is None:
            return 0
        return int(self._api_response.total_row_count)

    @total_row_count.setter
    def total_row_count(self, value: int):
        self._api_response.total_row_count = value

    @property
    def has_next_page(self) -> bool:
        """This checks to see if there is a next page

        Returns:
            bool: returns a bool value if there is a next page
        """
        return self._api_response["next_url"] is not None
