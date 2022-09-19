from typing import Any, List, Optional, Union

from pandas import DataFrame, concat

from cdapython.utils.none_check import none_check


class State:
    def __init__(
        self, df: Optional[DataFrame] = None, list_array: Optional[list] = None
    ) -> None:
        self.df: Union[DataFrame, None] = df
        self._list: Union[List[Any], None] = list_array

    def get_df(self) -> DataFrame:
        return none_check(self.df)

    def concat_df(self, dataframe: DataFrame) -> None:
        self.df = concat([dataframe, none_check(self.df)])

    def concat_list(self, value_list: list) -> None:
        list_not_none: List[Any] = none_check(value_list)
        none_check(self._list).extend(list_not_none)

    def get_list(self) -> list:
        return none_check(self._list)
