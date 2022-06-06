from datetime import datetime, timedelta
from functools import lru_cache, wraps
from typing import Any, Callable, Dict


def lru_cache_timed(seconds: int, maxsize: int = 128) -> Callable:
    def wrapper_cache(func: Any) -> Callable:
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args: tuple, **kwargs: Dict[str, Any]) -> Any:
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
