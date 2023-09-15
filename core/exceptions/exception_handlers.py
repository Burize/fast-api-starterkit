from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse
from core.exceptions import CustomException


async def not_found_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={"message": exc.message},
    )


async def not_authorized_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=HTTPStatus.UNAUTHORIZED,
        content={"message": 'Authorization error'},
    )


async def conflict_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content={"message": exc.message},
    )
