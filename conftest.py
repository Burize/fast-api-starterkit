import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.database.session import session_context
from core.inject import injector
from main import app
from testing.database_creator import DatabaseCreator


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='session', autouse=True)
def create_database():
    database_creator = injector.get(DatabaseCreator)
    database_creator.create()


@pytest.fixture(scope='function', autouse=True)
async def session():
    engine = injector.get(Engine)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    session = session_maker()
    token = session_context.set(session)

    await session.begin()
    yield
    await session.rollback()
    await session.close()

    session_context.reset(token)


@pytest.fixture(scope='function')
def api_client():
    return AsyncClient(app=app, base_url="http://test")
