from injector import CallableProvider
from injector import Module
from injector import singleton

from core.session import SessionStorage
from core.session import get_session_storage


class BaseConfiguration(Module):
    def configure(self, binder):
        binder.bind(SessionStorage, to=CallableProvider(get_session_storage), scope=singleton)
