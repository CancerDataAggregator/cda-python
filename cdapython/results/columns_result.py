from typing import Optional, Union, List
from pandas import DataFrame, json_normalize

from cdapython.results.base import BaseResult


class ColumnsResult(BaseResult):
    def __init__(
        self,
        show_sql: bool,
        show_count: bool,
        result: List,
        format_type: str = "json",
    ) -> None:
        self._result = result
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
            values: list["ColumnsResult"] = [
                list(i.keys())[0] for i in self._result if list(i.keys())[0] is not None
            ]
            # values = list(filter(None, values))
            if exact:
                return list(
                    filter(
                        lambda items: (str(items).lower() == filters.lower()),
                        values,
                    )
                )

            else:

                return list(
                    filter(
                        lambda items: (
                            str(items).lower().find(str(filters.lower())) != -1
                        ),
                        values,
                    )
                )
        return [list(i.keys())[0] for i in self._result]

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

        if record_path is None:
            return json_normalize(iter(self))

        return json_normalize(
            iter(self),
            max_level=max_level,
            record_path=record_path,
            meta=meta,
            meta_prefix=meta_prefix,
        )
