from fastapi import Request

from main import app


@app.middleware("http")
async def get_user_middleware(request: Request, call_next):
    response = await call_next(request)
    return response