from datetime import datetime, timedelta
from functools import lru_cache, wraps
from typing import Callable


def lru_cache_timed(seconds: int, maxsize: int = 128) -> Callable:
    if maxsize is None:
        maxsize = 128

    def wrapper_cache(func: lru_cache) -> Callable:
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
