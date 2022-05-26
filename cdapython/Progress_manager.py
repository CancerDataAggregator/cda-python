from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from rich.progress import Progress

if TYPE_CHECKING:
    from cdapython.results.Result import Result


TProgressManager = TypeVar("TProgressManager", bound="ProgressManager")


class ProgressManager:
    def __init__(self: TProgressManager, other: "Result", cls) -> None:
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
