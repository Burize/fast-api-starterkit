from fastapi import APIRouter
from fastapi import FastAPI

from core import settings
from core.exceptions import NotFoundException
from core.exceptions import NotAuthorizedException
from core.exceptions import ConflictException

from auth.routes import api_router as auth_router
from store.routes import api_router as store_router
from core.exceptions.exception_handlers import not_found_exception_handler
from core.exceptions.exception_handlers import not_authorized_exception_handler
from core.exceptions.exception_handlers import conflict_exception_handler
from core.middlewares import DBSessionMiddleware
from core.middlewares import UserSessionMiddleware


def init_app(app: FastAPI):
    if not settings.IS_TEST:
        app.add_middleware(DBSessionMiddleware)
    app.add_middleware(UserSessionMiddleware)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(NotAuthorizedException, not_authorized_exception_handler)
    app.add_exception_handler(ConflictException, conflict_exception_handler)

    root_router = APIRouter()
    root_router.include_router(auth_router)
    root_router.include_router(store_router)

    app.include_router(root_router, prefix=settings.API_PREFIX)
