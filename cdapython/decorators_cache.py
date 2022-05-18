from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import lru_cache, wraps
from typing import Any, Callable, Optional

from typing_extensions import TypedDict


def lru_cache_timed(seconds: int, maxsize: int = 128) -> Callable:
    if maxsize is None:
        maxsize = 128

    def wrapper_cache(func) -> Callable:
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.func_lru_cache.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
