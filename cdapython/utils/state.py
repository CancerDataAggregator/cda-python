from typing import Union, Optional

from cdapython.utils.none_check import none_check
from pandas import DataFrame, concat


class State:
    def __init__(
        self, df: Optional[DataFrame] = None, list: Optional[list] = None
    ) -> None:
        self.df = df
        self.list = list

    def get_df(self) -> DataFrame:
        return none_check(self.df)

    def concat_df(self, dataframe: DataFrame) -> None:
        self.df = concat([dataframe, self.df])

    def concat_list(self, list: list) -> None:
        self.list.extend(list)

    def get_list(self) -> list:
        return none_check(self.list)
