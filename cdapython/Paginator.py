"""
This module hold the Paginator class 
"""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Coroutine, List, TypeVar, Union

import anyio
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

from cdapython.utils.none_check import none_check

if TYPE_CHECKING:
    from pandas import DataFrame
    from rich.progress import TaskID

    from cdapython.results.columns_result import ColumnsResult
    from cdapython.results.page_result import Paged_Result
    from cdapython.results.string_result import StringResult


class Paginator:
    """
    This class helps the user page thought result objects
    """

    def __init__(
        self,
        result: Paged_Result,
        to_df: bool,
        to_list: bool,
        output: str,
        limit: int,
        format_type: str = "JSON",
        show_bar: bool = False,
    ) -> None:
        self.result: Union[Paged_Result, StringResult] = result
        self.to_df: bool = to_df
        self.to_list: bool = to_list
        self.limit: Union[int, None] = limit if limit else self.result._page_size
        self.count: int = self.result.count
        self.stopped: bool = False
        self.format_type: str = format_type
        self.output: str = output
        self.progress: Progress = Progress(
            TextColumn(text_format="[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            MofNCompleteColumn(),
        )
        self.show_bar: bool = show_bar
        self._loop: asyncio.AbstractEventLoop
        if self.show_bar:
            self.task: TaskID = self.progress.add_task(
                description="Processing", total=self.result.total_row_count
            )
            self.progress.update(task_id=self.task, advance=self.result.count)

    def _return_result(self) -> Union[DataFrame, List[Any], Paged_Result, StringResult]:
        """
        This return a Result object and DataFrame
        Returns:
            Union[DataFrame, list, Result]: _description_
        """
        var_output: str = none_check(object=self.output)
        if var_output == "full_df":
            return self.result.to_dataframe()
        if var_output == "full_list":
            return self.result.to_list()
        if self.to_df:
            return self.result.to_dataframe()
        if self.to_list:
            return self.result.to_list()

        return self.result

    def _do_next(self: Paginator) -> Union[DataFrame, List[Any], Paged_Result, None]:
        """
        This will check the next page and update the progress bar
        Returns:
            Union[DataFrame, List[Any], Paged_Result, None]
        """
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
                    for i in self.progress.tasks:
                        self.progress.remove_task(i.id)
                    self.progress.stop()
                raise e
        else:
            self.stopped = True
            return result_nx
        return None

    async def a_do_next(
        self,
    ) -> Coroutine[Any, Any, Union[DataFrame, List[Any], Paged_Result, None]]:
        return await anyio.to_thread.run_sync(self._do_next)

    def __iter__(self) -> Paginator:
        if self.show_bar:
            self.progress.start()
        return self

    def __aiter__(self) -> Paginator:
        self._loop = asyncio.get_event_loop()
        if self.show_bar:
            self.progress.start()
        return self

    async def __anext__(
        self,
    ) -> Coroutine[Any, Any, Union[DataFrame, List[Any], Paged_Result, None]]:
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

    def __next__(self) -> Union[List[Any], DataFrame, Paged_Result, None]:
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
                for i in self.progress.tasks:
                    self.progress.remove_task(i.id)
            raise e
        except KeyboardInterrupt as e:
            if self.show_bar:
                self.progress.console.clear_live()
                self.progress.stop()
                for i in self.progress.tasks:
                    self.progress.remove_task(i.id)
            raise e
