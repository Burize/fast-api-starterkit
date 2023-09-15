import pytest
from fastapi.testclient import TestClient

from core.inject import injector
from main import app
from testing.database_creator import DatabaseCreator


@pytest.fixture(scope='session', autouse=True)
def create_database():
    database_creator = injector.get(DatabaseCreator)
    database_creator.create()


@pytest.fixture(scope='session')
def api_client():
    return TestClient(app)
