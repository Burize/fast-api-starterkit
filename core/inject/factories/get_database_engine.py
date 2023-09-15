from sqlalchemy.ext.asyncio import create_async_engine

from core import settings


def get_database_engine():
    return create_async_engine(settings.DATABASE_URL)
