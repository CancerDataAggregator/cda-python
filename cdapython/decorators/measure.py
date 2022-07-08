from functools import wraps
from time import time
from typing import Any, Callable, Dict, Tuple, TypeVar, Union, cast

F = TypeVar("F", bound=Callable[..., Any])

FUNCTION_ANY = Union[F, Any]


class Measure:
    def __init__(self) -> None:
        self.kwargs: Dict[str, Any] = {}

    def __call__(self, func: F) -> FUNCTION_ANY:
        @wraps(func)
        def wrapper(*args: Tuple, **kwargs: Dict[str, Any]) -> FUNCTION_ANY:
            start_time = int(round(time() * 1000))
            self.kwargs = kwargs
            try:
                return func(*args, **kwargs)
            finally:
                if "verbose" not in self.kwargs or self.kwargs["verbose"] is True:
                    end_ = int(round(time() * 1000)) - start_time
                    print(f"Total execution time: {end_ if end_ > 0 else 0} ms")

        return wrapper
