from __future__ import annotations

from typing import TYPE_CHECKING, Union

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from typing_extensions import Self

from cdapython.utils.none_check import none_check

if TYPE_CHECKING:
    from pandas import DataFrame
    from rich.progress import TaskID

    from cdapython.results.result import Result


class Paginator:
    def __init__(
        self: Self,
        result: Result,
        to_df: bool,
        to_list: bool,
        to_collect_result: bool,
        output: str,
        limit: int,
        format_type: str = "JSON",
        show_bar: bool = False,
    ) -> None:
        self.result: Result = result
        self.to_df: bool = to_df
        self.to_list: bool = to_list
        self.to_collect_result: bool = to_collect_result
        self.limit: Union[int, None] = limit if limit else self.result._limit
        self.count: int = self.result.count
        self.stopped: bool = False
        self.format_type: str = format_type
        self.output: str = output
        self.progress: Progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            MofNCompleteColumn(),
        )
        self.show_bar: bool = show_bar
        if self.show_bar:
            self.task: TaskID = self.progress.add_task(
                "Processing", total=self.result.total_row_count
            )
            self.progress.update(self.task, advance=self.result.count)

    def _return_result(self) -> Union[DataFrame, list, Result]:
        var_output: str = none_check(self.output)
        if var_output == "full_df":
            return self.result.to_dataframe()
        if var_output == "full_list":
            return self.result.to_list()
        if self.to_df:
            return self.result.to_dataframe()
        if self.to_list:
            return self.result.to_list()
        if self.to_collect_result:
            return self.result
        return self.result

    def _do_next(self: Paginator) -> Union[DataFrame, list, Result, None]:
        result_nx = self._return_result()
        if self.result.has_next_page:
            try:
                tmp_result = self.result.next_page(limit=self.limit)
                if tmp_result:
                    self.result = tmp_result
                    if self.show_bar:
                        self.progress.update(self.task, advance=self.result.count)
                    return result_nx
            except Exception as e:
                if self.show_bar:
                    (self.progress.remove_task(i.id) for i in self.progress.tasks)
                    self.progress.stop()
                raise e
        else:
            self.stopped = True
            return result_nx

    async def a_do_next(self) -> Union[list, DataFrame, Result, None]:
        return self._do_next()

    def __iter__(self) -> Paginator:
        if self.show_bar:
            self.progress.start()
        return self

    def __aiter__(self) -> Paginator:
        if self.show_bar:
            self.progress.start()
        return self

    async def __anext__(self) -> Union[list, DataFrame, Result, None]:
        try:
            if self.stopped:
                if self.show_bar:
                    self.progress.update(self.task, advance=self.result.count)
                    self.progress.stop()
                raise StopAsyncIteration
            self.count += self.result.count
            return await self.a_do_next()
        except Exception as e:
            if self.show_bar:
                self.progress.stop()
            raise e

    def __next__(self) -> Union[list, DataFrame, Result, None]:
        try:
            if self.stopped:
                if self.show_bar:
                    self.progress.update(self.task, advance=self.result.count)
                    self.progress.stop()
                raise StopIteration
            self.count += self.result.count

            return self._do_next()
        except Exception as e:
            if self.show_bar:
                self.progress.console.clear_live()
                self.progress.stop()
                (self.progress.remove_task(i.id) for i in self.progress.tasks)
            raise e
        except KeyboardInterrupt as e:
            if self.show_bar:
                self.progress.console.clear_live()
                self.progress.stop()
                (self.progress.remove_task(i.id) for i in self.progress.tasks)
            raise e
