from fastapi import Request
from fastapi.responses import JSONResponse
from core.exceptions import CustomException


async def not_found_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )


async def not_authorized_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=401,
        content={"message": 'Authorization error'},
    )
