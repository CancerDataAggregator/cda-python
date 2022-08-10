from typing import Any, List, Union, Optional
from cdapython.utils.none_check import none_check
from pandas import DataFrame, concat


class State:
    def __init__(
        self, df: Optional[DataFrame] = None, _list: Optional[list] = None
    ) -> None:
        self.df: Union[DataFrame, None] = df
        self._list: Union[List[Any], None] = _list

    def get_df(self) -> DataFrame:
        return none_check(self.df)

    def concat_df(self, dataframe: DataFrame) -> None:
        self.df = concat([dataframe, none_check(self.df)])

    def concat_list(self, value_list: list) -> None:
        list_not_none: List[Any] = none_check(value_list)
        none_check(self._list).extend(list_not_none)

    def get_list(self) -> list:
        return none_check(self._list)
