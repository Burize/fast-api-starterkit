from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession

session_context: ContextVar[AsyncSession] = ContextVar("_session", default=None)


def get_session() -> AsyncSession:
    _session = session_context.get()
    if _session is None:
        raise Exception('There is no Session in the current context')

    return _session


class SessionMeta(type):
    def __getattr__(self, key):
        return getattr(get_session(), key)


class _Session(metaclass=SessionMeta):
    pass


Session: AsyncSession = _Session
