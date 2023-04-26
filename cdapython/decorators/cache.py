"""
This file is made for caching decorators
"""
from datetime import datetime, timedelta
from functools import lru_cache, wraps
from typing import Any, Callable, Dict, Tuple


def lru_cache_timed(seconds: int = 10, maxsize: int = 128) -> Callable:
    """
    lru_cache_timed This function is made to cache
    the values for the defaults to 10 seconds

    Args:
        seconds (int): _description_ Defaults to 10
        maxsize (int, optional): _description_. Defaults to 128.

    Returns:
        Callable: _description_
    """

    def wrapper_cache(func: Any) -> Callable:
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args: Tuple[Any, Any], **kwargs: Dict[str, Any]) -> Any:
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
