from fastapi import APIRouter
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from core import settings
from core.exceptions import NotFoundException
from core.exceptions import NotAuthorizedException

from auth.routes import api_router as auth_router
from core.exceptions.exception_handlers import not_found_exception_handler
from core.exceptions.exception_handlers import not_authorized_exception_handler


def init_app(app: FastAPI):
    app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL, commit_on_exit=True)
    app
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(NotAuthorizedException, not_authorized_exception_handler)

    root_router = APIRouter()
    root_router.include_router(auth_router)

    app.include_router(root_router, prefix=settings.API_PREFIX)

