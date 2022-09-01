from typing import Optional, Union, List
from pandas import DataFrame

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
