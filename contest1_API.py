from functools import wraps
from typing import Callable, TypeVar
T = TypeVar("T")

class UnsupportedValueError(Exception):
    pass


class NonExistedKeyError(Exception):
    pass
exception_mapping = {
    ValueError: UnsupportedValueError,
    KeyError: NonExistedKeyError,
}


def api_computable_exceptions(
    exception_mapping: dict[type[Exception], type[Exception]]
) -> Callable[[T], T]:
    def decorator(func):
        def wrapper(*args,**kwargs):
            try:
                func(*args,**kwargs)
            except Exception as exeption:
                if type(exeption) in exception_mapping:
                    raise exception_mapping[type(exeption)] from None
                else:
                    raise exeption
        return wrapper
    return decorator


@api_computable_exceptions(exception_mapping)
def raise_value_error() -> None:
    raise ValueError


@api_computable_exceptions(exception_mapping)
def raise_key_error() -> None:
    raise KeyError

@api_computable_exceptions(exception_mapping)
def raise_type_error() -> None:
    raise TypeError

@api_computable_exceptions(exception_mapping)
def raise_exception() -> None:
    raise Exception



try:
    raise_value_error()
    assert False
except UnsupportedValueError:
    pass

try:
    raise_key_error()
    assert False
except NonExistedKeyError:
    pass

try:
    raise_exception()
except Exception as exc:
    assert isinstance(exc, Exception)
    
try:
    raise_type_error()
    assert False
except TypeError:
    pass