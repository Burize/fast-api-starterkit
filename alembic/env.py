import os
import sys
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context


APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APPS_DIR)

from core.database.base import Base
from core.utils.discover_modules import discover_modules

discover_modules('**/models')

target_metadata = Base.metadata
sys.path.remove(APPS_DIR)


config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    db_url = os.getenv('DATABASE_URL', '').replace('+asyncpg', '')

    engine = create_engine(db_url)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            transaction_per_migration=True,
        )
        context.run_migrations()


run_migrations_online()
