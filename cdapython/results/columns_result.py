from typing import Any, List, Optional, Union
from typing_extensions import Literal, TypedDict

from pandas import DataFrame, json_normalize, merge, Index

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
        self, filters: Optional[str] = None, exact: bool = False, endpoint: str = ""
    ) -> list:
        if filters is not None and filters != "":
            values: Optional[List[_Column_Types]] = None
            filters: str = filters.replace("\n", " ").strip()
            if self.description is False:
                values = [
                    i["fieldName"] for i in self._result if i["fieldName"] is not None
                ]
            if self.description:
                values = [i for i in self._result if list(i) is not None]
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

        return [i for i in self._result]

    def to_dataframe(
        self,
        record_path: Optional[Union[str, list]] = None,
        meta: Optional[Union[str, List[Union[str, List[str]]]]] = None,
        meta_prefix: Optional[str] = None,
        max_level: Optional[int] = None,
        search_fields: Optional[Union[_Column_str, List[_Column_str]]] = None,
        search_value: Optional[str] = None,
    ) -> DataFrame:
        """[summary]
        Creates a pandas DataFrame for the Results

        Returns:
            DataFrame: [description]
        """

        self._data_table: dict[str, list[Any]] = json_normalize(self._result)

        if search_fields is not None:
            column_names = ["fieldName", "endpoint", "description", "type", "mode"]
            search_fields = search_fields
            search_value = search_value
            df = DataFrame(self._data_table)
            value = DataFrame(columns=column_names, index=Index([], dtype="int"))

            for i in search_fields:
                value = merge(
                    value,
                    df[df[i].str.contains(search_value, case=False, na=False)],
                    how="right",
                    right_on=column_names,
                    left_on=column_names,
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
