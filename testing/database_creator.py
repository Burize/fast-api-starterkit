import os

from sqlalchemy import create_engine
from sqlalchemy import text

from core import settings
import re
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from core.database.base import Base

TEST_DATABASE_NAME = 'test_fastapi_starterkit'


class DatabaseCreator:
    def create(self):
        db_url = os.getenv('DATABASE_URL').replace('+asyncpg', '')
        engine = create_engine(db_url)
        engine.raw_connection().set_isolation_level(
            ISOLATION_LEVEL_AUTOCOMMIT
        )

        with engine.connect() as connection:
            connection.execute(text(f"DROP DATABASE IF EXISTS {TEST_DATABASE_NAME}"))
            connection.execute(text(f"CREATE DATABASE {TEST_DATABASE_NAME}"))
        engine.dispose()

        test_db_url = self.get_test_database_url(db_url)

        engine = create_engine(test_db_url.replace('+asyncpg', ''))
        Base.metadata.create_all(engine)

        settings.DATABASE_URL = test_db_url

    def get_test_database_url(self, db_url: str):
        db_credentials = re.search('//.*/', db_url).group()
        return f'postgresql+asyncpg:{db_credentials}{TEST_DATABASE_NAME}'
