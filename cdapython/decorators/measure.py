"""
This is the time decorator class
"""
from functools import wraps
from time import time
from typing import Any, Callable, Dict, Tuple, TypeVar, Union

F = TypeVar("F", bound=Callable[..., Any])

FunctionAny = Union[F, Any]


class Measure:
    """
    This class will Measure time execution.
    """

    def __init__(self) -> None:
        self.kwargs: Dict[str, Any] = {}
        self.result: Union[Any, None]

    def __call__(self, func: F) -> FunctionAny[F]:
        self.result = None

        @wraps(func)
        def wrapper(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> FunctionAny[F]:
            start_time = int(round(time() * 1000))
            self.kwargs = kwargs
            try:
                self.result = func(*args, **kwargs)
                return self.result
            finally:
                if self.result is not None:
                    if "verbose" not in self.kwargs or self.kwargs["verbose"] is True:
                        end_ = int(round(time() * 1000)) - start_time
                        seconds = round((end_ / 1000) % 60, 3)
                        minutes = round(int((end_ / (1000 * 60)) % 60))
                        print(
                            f"""
                            Total execution time: {minutes if minutes > 0 else 0}
                            min {seconds if seconds > 0 else 0} sec {end_ if end_ > 0 else 0} ms
                            """
                        )

        return wrapper

    def __str__(self) -> str:
        return self.__class__.__name__
