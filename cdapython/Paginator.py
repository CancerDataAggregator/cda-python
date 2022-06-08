from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar, Union

from cdapython.progress_manager import ProgressManager

if TYPE_CHECKING:
    from pandas import DataFrame

    from cdapython.results.result import Result


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

    def _do_next(self: Paginator) -> Union[dict, list, DataFrame, Result]:
        result_nx: "Result" = self.result

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

    async def a_do_next(self) -> Union[dict, list, DataFrame, Result]:

        return self._do_next()

    def __iter__(self) -> "Paginator":
        return self

    def __aiter__(self) -> "Paginator":
        return self

    async def __anext__(self) -> Optional[Union["DataFrame", "Result"]]:
        if self.stopped:
            raise StopAsyncIteration

        return await self.a_do_next()

    def __next__(self) -> Optional[Union[DataFrame, Result]]:
        if self.stopped:
            raise StopIteration
        self.count += self.result.count

        return self._do_next()
