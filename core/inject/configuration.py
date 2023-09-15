from injector import CallableProvider
from injector import Module
from injector import singleton
from sqlalchemy import Engine

from core.inject.factories import get_session_storage
from core.inject.factories import get_database_engine
from core.session import SessionStorage


class BaseConfiguration(Module):
    def configure(self, binder):
        binder.bind(SessionStorage, to=CallableProvider(get_session_storage), scope=singleton)
        binder.bind(Engine, to=CallableProvider(get_database_engine), scope=singleton)


class Configuration(BaseConfiguration):
    pass


class TestConfiguration(BaseConfiguration):
    def configure(self, binder):
        super().configure(binder)
        binder.bind(Engine, to=CallableProvider(get_database_engine))
