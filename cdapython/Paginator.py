from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar, Union

if TYPE_CHECKING:
    from pandas import DataFrame

    from cdapython.Result import Result


TPaginator = TypeVar("TPaginator", bound="Paginator")


class Paginator:
    def __init__(
        self: TPaginator,
        result: "Result",
        to_df: bool,
        to_list: bool,
        to_dict: bool,
        format_type: str = "JSON",
    ) -> None:
        self.result = result
        self.to_df = to_df
        self.to_list = to_list
        self.to_dict = to_dict
        self.count = 0
        self.stopped = False
        self.format_type = format_type

    def __iter__(self) -> "Paginator":
        return self

    def __aiter__(self) -> "Paginator":
        return self

    async def __anext__(self) -> Optional[Union["DataFrame", "Result"]]:
        if self.stopped:
            raise StopAsyncIteration
        result_nx = self.result

        if self.to_df:
            result_nx = self.result.to_dataframe()
        if self.to_list and self.result is not None:
            result_nx = self.result.to_list()
        if self.to_dict and self.result is not None:
            result_nx = self.result.to_dict()
        if self.result.has_next_page:
            self.result = self.result.next_page()
            return result_nx
        else:
            self.stopped = True
            return result_nx

    def __next__(self) -> Optional[Union[DataFrame, Result]]:
        if self.stopped:
            raise StopIteration
        self.count += self.result.count

        # print(
        #     f"Row {self.count} out of {self.result.total_row_count} {int((self.count/self.result.total_row_count)*100)}%"
        # )
        result_nx = self.result

        if self.to_df:
            result_nx = self.result.to_dataframe()

        if self.result.has_next_page:
            self.result = self.result.next_page()
            return result_nx
        else:
            self.stopped = True
            return result_nx
