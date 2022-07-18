from typing import TypeVar, Union

T = TypeVar("T")


def none_check(object: Union[T, None]) -> T:
    """Checks that an object is not None
    This fixes mypy errors by removing any `Optional` tags
    Args:
        object: An object to be checked
    Returns:
        The object that was passed in, if not None
    Raises:
        AssertionError: when `object` is None
    """
    if object is None:
        raise AssertionError(f"{object} is None!")

    return object
