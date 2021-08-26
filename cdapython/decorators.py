from functools import wraps
from time import time


def measure(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start_time = int(round(time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time() * 1000)) - start_time
            print(f"Total execution time: {end_ if end_ > 0 else 0} ms")

    return _time_it
