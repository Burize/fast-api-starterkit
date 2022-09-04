from fastapi import APIRouter
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from auth.routes import api_router as auth_router
import core.settings as settings

app = FastAPI(
    title='starter', docs_url=f"{settings.API_PREFIX}/docs"
)

app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)

root_router = APIRouter()
root_router.include_router(auth_router)


app.include_router(root_router, prefix=settings.API_PREFIX)
