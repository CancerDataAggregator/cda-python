from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar, Union


from rich.progress import Progress

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
        format_type: str = "JSON",
    ) -> None:
        self.result = result
        self.to_df = to_df
        self.to_list = to_list
        self.count = self.result.count
        self.stopped = False
        self.format_type = format_type
        self.progress = Progress()
        self.task = self.progress.add_task(
            "Processing", total=self.result.total_row_count
        )
        self.progress.update(self.task, advance=self.result.count)

    def _do_next(self: Paginator) -> Union[dict, list, DataFrame, Result]:

        result_nx: "Result" = self.result

        if self.to_df:
            result_nx = self.result.to_dataframe()
        if self.to_list and self.result is not None:
            result_nx = self.result.to_list()
        if self.result.has_next_page:
            try:
                self.result = self.result.next_page()
                self.progress.update(self.task, advance=self.result.count)
                return result_nx
            except Exception as e:
                self.progress.stop_task()
                self.progress.stop()
                raise e
        else:
            self.stopped = True
            return result_nx

    async def a_do_next(self) -> Union[dict, list, DataFrame, Result]:

        return self._do_next()

    def __iter__(self) -> "Paginator":
        self.progress.start()
        return self

    def __aiter__(self) -> "Paginator":
        self.progress.start()
        return self

    async def __anext__(self) -> Optional[Union["DataFrame", "Result"]]:
        if self.stopped:
            self.progress.update(self.task, advance=self.result.count)
            self.progress.stop()
            raise StopAsyncIteration
        self.count += self.result.count
        return await self.a_do_next()

    def __next__(self) -> Optional[Union[DataFrame, Result]]:
        if self.stopped:
            self.progress.update(self.task, advance=self.result.count)
            self.progress.stop()
            raise StopIteration
        self.count += self.result.count

        return self._do_next()
