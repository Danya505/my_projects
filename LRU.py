from typing import (
    Callable,
    TypeVar,
)

from collections import OrderedDict


T = TypeVar("T")


def lru_cache(capacity: int) -> Callable[[T], T]:
    if not ((isinstance(capacity, int) or isinstance(capacity, float))):
        raise TypeError
    capacity = round(capacity)
    if capacity < 1:
        raise ValueError

    def decorator(func):

        cache = OrderedDict()

        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs))
            if key in cache:
                cache.move_to_end(key)
                return cache[key]
            result = func(*args, *kwargs)
            if len(cache) < capacity:
                cache[key] = result
                cache.move_to_end(key)
            else:
                cache.popitem(last=False)
                cache[key] = result
                cache.move_to_end(key)

            return result
        return wrapper
    return decorator
