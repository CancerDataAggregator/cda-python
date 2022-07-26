from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar, Union


from rich.progress import (
    Progress,
    MofNCompleteColumn,
    TimeElapsedColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)

from cdapython.utils.none_check import none_check

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
        output: str,
        limit: int,
        format_type: str = "JSON",
    ) -> None:
        self.result = result
        self.to_df = to_df
        self.to_list = to_list
        self.limit = limit if limit else self.result._limit
        self.count = self.result.count
        self.stopped = False
        self.format_type = format_type
        self.output = output
        self.progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            MofNCompleteColumn(),
        )

        self.task = self.progress.add_task(
            "Processing", total=self.result.total_row_count
        )
        self.progress.update(self.task, advance=self.result.count)

    def _do_next(self: Paginator) -> Union[dict, list, DataFrame, Result]:

        result_nx: "Result" = none_check(self.result)
        self.output = none_check(self.output)
        if self.output == "full_df":
            result_nx = self.result.to_dataframe()
        if self.output == "full_list":
            result_nx = self.result.to_list()
        if self.to_df:
            result_nx = self.result.to_dataframe()
        if self.to_list and self.result is not None:
            result_nx = self.result.to_list()
        if self.result.has_next_page:
            try:
                self.result = self.result.next_page(limit=self.limit)
                self.progress.update(self.task, advance=self.result.count)
                return result_nx
            except Exception as e:
                (self.progress.remove_task(i.id) for i in self.progress.tasks)
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
        try:
            if self.stopped:
                self.progress.update(self.task, advance=self.result.count)
                self.progress.stop()
                raise StopAsyncIteration
            self.count += self.result.count
            return await self.a_do_next()
        except Exception as e:
            self.progress.stop()
            raise e

    def __next__(self) -> Optional[Union[DataFrame, Result]]:
        try:
            if self.stopped:
                self.progress.update(self.task, advance=self.result.count)
                self.progress.stop()
                raise StopIteration
            self.count += self.result.count

            return self._do_next()
        except Exception as e:
            self.progress.console.clear_live()
            self.progress.stop()
            (self.progress.remove_task(i.id) for i in self.progress.tasks)
            raise e
        except KeyboardInterrupt as e:
            self.progress.console.clear_live()
            self.progress.stop()
            (self.progress.remove_task(i.id) for i in self.progress.tasks)
            raise e
