from __future__ import annotations

from re import I
from typing import TYPE_CHECKING, Any, TypeVar

from rich.progress import Progress

if TYPE_CHECKING:
    from cdapython.Paginator import Paginator
    from cdapython.results.result import Result


TProgressManager = TypeVar("TProgressManager", bound="ProgressManager")
T = TypeVar("T", bound="Paginator")


class ProgressManager:
    def __init__(self: TProgressManager, other: "Result", cls: T) -> None:
        self.count = other._limit
        self.total = other.total_row_count
        self.cls = cls
        self.__call__()

    def __iter__(self: TProgressManager) -> Any:
        return self.cls

    def __call__(self: TProgressManager) -> Any:
        with Progress() as progress:
            task = progress.add_task("Processing", total=self.total)
            progress.update(task, advance=self.count)
            return self.cls
