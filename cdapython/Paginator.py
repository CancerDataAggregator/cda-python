"""
This module hold the Paginator class 
"""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Coroutine, List, Optional, Union

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

    from cdapython.results.page_result import Paged_Result
    from cdapython.results.result import Result
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
        show_counts: bool = False,
    ) -> None:
        print("ran Paginator.py __init__")
        self.result: Union[Paged_Result, StringResult] = result
        self.to_df: bool = to_df
        self.to_list: bool = to_list
        self.limit: Union[int, None] = limit if limit else self.result._limit
        self.stopped: bool = False
        self.format_type: str = format_type
        self.output: str = output
        self.total_result: int = 0
        self.progress_dirty: bool = False
        self.show_counts: bool = show_counts
        self.progress: Progress = Progress(
            TextColumn(text_format="[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            MofNCompleteColumn(),
        )
        self.progress.live._screen = True
        self.task: Optional[TaskID] = None
        self.show_bar: bool = show_bar

    def _return_result(self) -> Union[DataFrame, List[Any], Paged_Result, StringResult]:
        """
        This return a Result object and DataFrame
        Returns:
            Union[DataFrame, list, Result]: _description_
        """
        print("ran Paginator.py _return_result")
        var_output: str = none_check(self.output)
        if var_output == "full_df":
            return self.result.to_dataframe()
        if var_output == "full_list":
            return self.result.to_list()
        if self.to_df:
            return self.result.to_dataframe()
        if self.to_list:
            return self.result.to_list()

        return self.result

    def _do_next(self: Paginator) -> Union[DataFrame, List[Any], Result, None]:
        print("ran Paginator.py _do_next")
        if self.result.has_next_page or not self.stopped:
            try:
                tmp_result = self.result.next_page(
                    limit=self.limit, show_counts=self.show_counts
                )
                if tmp_result:
                    self.result = tmp_result
                    if self.show_bar:
                        if self.task is None:
                            self.task = self.progress.add_task(
                                "Processing", total=self.result.total_row_count
                            )

                        self.progress.update(
                            task_id=self.task,
                            advance=self.result.count,
                            refresh=True,
                        )
                    if self.result.has_next_page == False:
                        self.stopped = True
                    if self.output != "":
                        return self._return_result()
                    return self.result
            except Exception as e:
                if self.show_bar:
                    self.progress.update(
                        task_id=self.task, advance=self.result.count, refresh=True
                    )
                    for i in self.progress.tasks:
                        self.progress.remove_task(task_id=i.id)
                    self.progress.stop()
                raise e
        return self.result

    async def a_do_next(self) -> Union[List, DataFrame, Result, None]:
        print("ran Paginator.py a_do_next")
        return self._do_next()

    def __iter__(self) -> Paginator:
        print("ran Paginator.py __iter__")
        if self.show_bar:
            self.progress.start()
        return self

    def __aiter__(self) -> Paginator:
        print("ran Paginator.py __aiter__")
        self._loop = asyncio.get_event_loop()
        if self.show_bar:
            self.progress.start()
        return self

    async def __anext__(
        self,
    ) -> Coroutine[Any, Any, Union[DataFrame, List[Any], Paged_Result, None]]:
        print("ran Paginator.py __anext__")
        try:
            if self.stopped:
                if self.show_bar:
                    if self.task:
                        self.progress.update(self.task, advance=self.result.count)
                        self.progress.stop()
                raise StopAsyncIteration
            return await self.a_do_next()
        except Exception as e:
            if self.show_bar:
                self.progress.stop()
            raise e

    def __next__(self) -> Union[List[Any], DataFrame, Paged_Result, None]:
        print("ran Paginator.py __next__")
        try:
            if self.stopped:
                if self.show_bar:
                    if self.task:
                        self.progress.update(self.task, advance=self.result.count)
                        self.progress.stop()
                raise StopIteration
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
