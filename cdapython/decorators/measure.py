"""
This is the time decorator class
"""
from functools import wraps
from time import time
from typing import Any, Callable, Dict, Tuple, TypedDict, TypeVar, Union

F = TypeVar("F", bound=Callable[..., Any])

FunctionAny = Union[F, Any]


class Measure_Type(TypedDict):
    verbose: Union[bool, None]


class Measure:
    """
    This class will Measure time execution.
    """

    def __init__(self, verbose: bool = False) -> None:
        print("ran measure.py __init__")
        self.kwargs: Measure_Type = {"verbose": verbose}
        self.result: Union[Any, None]
        self.verbose_default: bool = verbose

    def __call__(self, func: F) -> FunctionAny[F]:
        print("ran measure.py __call__")
        self.result = None

        @wraps(func)
        def wrapper(*args: Tuple[Any], **kwargs: Measure_Type) -> FunctionAny[F]:
            print("ran measure.py wrapper")
            start_time = int(round(time() * 1000))
            self.kwargs = kwargs
            verbose = self.verbose_default
            if "verbose" in self.kwargs:
                verbose = self.kwargs.get("verbose")

            try:
                self.result = func(*args, **kwargs)
                return self.result
            finally:
                if self.result is not None:
                    if verbose:
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
        print("ran measure.py __str__")
        return self.__class__.__name__
