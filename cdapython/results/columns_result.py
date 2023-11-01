from typing import Any, Dict, List, Optional, Union

from pandas import DataFrame, Index, json_normalize, merge
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
    mode: str


_Column_str = Union[
    Literal["fieldName"], Literal["endpoint"], Literal["description"], Literal["mode"]
]


class ColumnsResult(BaseResult):
    def __init__(
        self,
        show_sql: bool,
        show_count: bool,
        result: List[Any],
        description: bool = True,
        format_type: str = "json",
    ) -> None:
        self._result = result
        self.description = description
        self._data_table: DataFrame
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
        self, filters: Optional[str] = None, exact: bool = False, endpoint: str = ""
    ) -> List[Any]:
        if filters is not None and filters != "":
            values: Union[List[_Column_Types], List[Any]] = []
            filters = filters.replace("\n", " ").strip()
            if self.description is False:
                values.extend(
                    [i["fieldName"] for i in self._result if i["fieldName"] is not None]
                )
            if self.description:
                values.extend([i for i in self._result if list(i) is not None])
            # values = list(filter(None, values))
            if exact:
                if self.description is False:
                    return list(
                        filter(
                            lambda items: (
                                str(items["fieldName"]).lower() == filters.lower()
                            ),
                            values,
                        )
                    )
                return list(
                    filter(
                        lambda items: (
                            str(items["description"]).lower() == filters.lower()
                            or str(items["endpoint"]).lower() == filters.lower()
                            or str(items["fieldName"]).lower() == filters.lower()
                        ),
                        values,
                    )
                )
            else:
                if self.description is False:
                    return list(
                        filter(
                            lambda items: (
                                str(items).lower().find(str(filters.lower())) != -1
                            ),
                            values,
                        )
                    )
                return list(
                    filter(
                        lambda items: (
                            str(items["description"]).lower().find(filters.lower())
                            != -1
                            or str(items["endpoint"]).lower().find(filters.lower())
                            != -1
                            or str(items["fieldName"]).lower().find(filters.lower())
                            != -1
                        ),
                        values,
                    )
                )
        if self.description is False:
            return [i["fieldName"] for i in self._result]

        return list(self._result)

    def to_dataframe(
        self,
        record_path: Union[Union[str, List[Any]], None] = None,
        meta: Union[str, List[Union[str, List[str]]], None] = None,
        meta_prefix: Union[str, None] = None,
        max_level: Union[int, None] = None,
        search_fields: Union[List[str], str, None] = None,
        search_value: str = "",
    ) -> DataFrame:
        """[summary]
        Creates a pandas DataFrame for the Results

        Returns:
            DataFrame: [description]
        """

        self._data_table: DataFrame = json_normalize(self._result)

        if search_fields is not None:
            column_names = [
                "fieldName",
                "endpoint",
                "description",
                "type",
                "isNullable",
            ]
            data_frame = self._data_table
            value = DataFrame(columns=column_names, index=Index([], dtype="int"))
            if isinstance(search_fields, str):
                search_fields = [search_fields]
            for i in search_fields:
                value = merge(
                    value,
                    data_frame[
                        data_frame[i].str.contains(search_value, case=False, na=False)
                    ],
                    how="right",
                    right_on=column_names,
                    left_on=column_names,
                )
            return value
        if self.format_type == "tsv":
            return self._df

        if self.description is False:
            data_table: Dict[str, List[Any]] = {
                "fieldName": [i["fieldName"] for i in self._result]
            }
            return DataFrame(data_table)

        return DataFrame(self._data_table)
