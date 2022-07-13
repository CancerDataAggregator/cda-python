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
    def __init__(self: TProgressManager, cls) -> None:
        self.count = cls.result._limit
        self.total = cls.result.total_row_count
        self.cls = cls
        _, self.task = self.__call__()

    def __iter__(self: TProgressManager) -> Any:
        return self.cls

    def __call__(self: TProgressManager) -> Any:
        

    def return_cls(self) -> Any:
        return (self.cls, self.task)
