import functools
from typing import Callable
from typing import Type

from fastapi import HTTPException

from core.exceptions import CustomException


def exception_to_response(exception_type: Type[CustomException], http_code: int):
    def decorator(func: Callable):

        @functools.wraps(func)
        def wrapped_func(*args, **kwarg):
            try:
                return func(*args,  **kwarg)
            except exception_type as exc:
                raise HTTPException(detail=exc.message, status_code=http_code)

        return wrapped_func
    return decorator
