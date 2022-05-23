from typing import TYPE_CHECKING, TypeVar
from rich.progress import Progress
from __future__ import annotations

if TYPE_CHECKING:
    from cdapython.Result import Result


TypeVar


class ProgressManager:
    def __init__(self, other: "Result", cls) -> None:
        self.count = other._limit
        self.total = other.total_row_count
        self.cls = cls
        self.__call__()

    def __iter__(self):
        return self.cls

    def __call__(self):
        with Progress() as progress:
            task = progress.add_task("Processing", total=self.total)
            progress.update(task, advance=self.count)
            return self.cls
