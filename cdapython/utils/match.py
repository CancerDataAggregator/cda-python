from __future__ import annotations

try:
    # Use the match statement from Python 3.10 if available

    from typing import Any, Callable, TypeVar

    T = TypeVar("T")

    def match(value: T, *cases: tuple[T, Callable[[], Any]]) -> Any:
        for case, action in cases:
            if case == value:
                return action()

        raise ValueError(f"No match found for value: {value}")

except ImportError:
    # Define a match function for Python 3.8

    def match(value, *cases):
        for case, action in cases:
            if case == value:
                return action()

        raise ValueError("No match found for value: {}".format(value))
