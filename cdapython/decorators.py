import asyncio
from functools import wraps
from time import time


def create_async_func(f):
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)

    return wrapper


class measure:
    def __init__(self) -> None:
        self.kwargs = None

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = int(round(time() * 1000))
            self.kwargs = kwargs
            try:
                return func(*args, **kwargs)
            finally:
                if "verbose" not in self.kwargs or self.kwargs["verbose"] is True:
                    end_ = int(round(time() * 1000)) - start_time
                    print(f"Total execution time: {end_ if end_ > 0 else 0} ms")

        return wrapper
