from typing import Any, List, Optional, Union

from pandas import DataFrame, Index, json_normalize, concat
from typing_extensions import Literal, TypedDict

from cdapython.results.base import BaseResult


class _Column_Types(TypedDict):
    """
    This is made for typechecking a dict
    Args:
        TypedDict (_type_): _description_
    """

    fieldName: str
    endpoint: str
    description: str
    type: str
    mode: str


_Column_str = Union[
    Literal["fieldName"], Literal["endpoint"], Literal["description"], Literal["mode"]
]


class ColumnsResult(BaseResult):
    def __init__(
        self,
        show_sql: bool,
        show_count: bool,
        result: List,
        description: bool = True,
        format_type: str = "json",
    ) -> None:
        self._result = result
        self.description = description
        super().__init__(
            show_sql=show_sql,
            show_count=show_count,
            format_type=format_type,
            result=result,
        )

    def _repr_value(self, show_value: Optional[bool]) -> str:
        return f"""Number of Fields {len(self._result)}"""

    def __repr__(self) -> str:
        return self._repr_value(show_value=self.show_sql)

    def __str__(self) -> str:
        return self._repr_value(show_value=self.show_sql)

    def to_list(
        self,
        search_fields: Optional[Union[str, List[str]]] = None,
        search_value: Optional[str] = None,
        allow_substring: bool = True,
    ) -> list:
        """_summary_

        Args:
            allow_substring (bool, optional): Whether the seach_value should match if it is only part of a word. Defaults to True.
            search_fields (Optional[Union[str, List[str]]], optional): _description_. Defaults to None.
            search_value (Optional[str], optional): _description_. Defaults to None.

        Returns:
            list: _description_
        """
        result = self.to_dataframe(
            search_fields=search_fields,
            search_value=search_value,
            allow_substring=allow_substring,
        )
        if self.description is False:
            return result["fieldName"].values.tolist()
        return list(result.to_dict("records"))

    def to_dataframe(
        self,
        record_path: Optional[Union[str, list]] = None,
        meta: Optional[Union[str, List[Union[str, List[str]]]]] = None,
        meta_prefix: Optional[str] = None,
        max_level: Optional[int] = None,
        search_fields: Optional[Union[_Column_str, List[_Column_str]]] = None,
        search_value: Optional[str] = None,
        allow_substring: bool = True,
    ) -> DataFrame:
        """[summary]
        Creates a pandas DataFrame for the Results

        Returns:
            DataFrame: [description]
        """

        self._data_table: DataFrame = json_normalize(self._result)

        if search_fields is not None:
            column_names = ["fieldName", "endpoint", "description", "type", "mode"]
            search_fields = search_fields
            search_value = search_value
            df = self._data_table
            value = DataFrame(columns=column_names, index=Index([], dtype="int"))
            if isinstance(search_fields, str):
                search_fields = [search_fields]
            if allow_substring:
                for i in search_fields:
                    value = (
                        concat(
                            [
                                value,
                                df[
                                    df[i].str.contains(
                                        search_value, case=False, na=False
                                    )
                                ],
                            ]
                        )
                        .drop_duplicates()
                        .reset_index(drop=True)
                    )
            else:
                for i in search_fields:
                    value = (
                        concat([value, df[df[i].str.lower() == search_value.lower()]])
                        .drop_duplicates()
                        .reset_index(drop=True)
                    )
            return value
        if self.format_type == "tsv":
            return self._df

        if self.description is False:
            data_table: dict[str, list[Any]] = {
                "fieldName": [i["fieldName"] for i in self._result]
            }
            return DataFrame(data_table)

        return DataFrame(self._data_table)
