from typing import Optional, Union, List
from pandas import DataFrame, json_normalize

from cdapython.results.base import BaseResult


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

    def to_list(self, filters: Optional[str] = None, exact: bool = False) -> list:
        if filters is not None and filters != "":

            filters: str = filters.replace("\n", " ").strip()
            if self.description is False:
                values: list["ColumnsResult"] = [
                    list(i.keys())[0]
                    for i in self._result
                    if list(i.keys())[0] is not None
                ]
            if self.description:
                values: list["ColumnsResult"] = [
                    i for i in self._result if list(i.keys())[0] is not None
                ]
            # values = list(filter(None, values))
            if exact:
                if self.description is False:
                    return list(
                        filter(
                            lambda items: (str(items).lower() == filters.lower()),
                            values,
                        )
                    )
                return list(
                    filter(
                        lambda items: (
                            str(list(items.keys())[0]).lower() == filters.lower
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
                            str(list(items.keys())[0]).lower().find(filters.lower())
                            != -1
                        ),
                        values,
                    )
                )
        if self.description is False:
            return [list(i.keys())[0] for i in self._result]
        return [i for i in self._result]

    def to_dataframe(
        self,
        record_path: Optional[Union[str, list]] = None,
        meta: Optional[Union[str, List[Union[str, List[str]]]]] = None,
        meta_prefix: Optional[str] = None,
        max_level: Optional[int] = None,
    ) -> DataFrame:
        """[summary]
        Creates a pandas DataFrame for the Results

        Returns:
            DataFrame: [description]
        """
        if self.format_type == "tsv":
            return self._df

        if self.description is False:
            data_table = {"Column_Name": [list(i.keys())[0] for i in self._result]}
            return DataFrame(data_table)

        data_table = {
            "Column_Name": [list(i.keys())[0] for i in self._result],
            "Description": [list(i.values())[0] for i in self._result],
        }

        return DataFrame(data_table)
