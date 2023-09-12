from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from core import settings

from sqlalchemy.ext.asyncio import create_async_engine
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp

_SessionMaker: async_sessionmaker = None
_session_context: ContextVar[AsyncSession] = ContextVar("_session", default=None)


class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self,app: ASGIApp):
        super().__init__(app)
        global _SessionMaker
        engine = create_async_engine(settings.DATABASE_URL)
        _SessionMaker = async_sessionmaker(engine, expire_on_commit=False)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        async with DBSessionContext():
            response = await call_next(request)
        return response


class DBSessionContext:
    def __init__(self):
        self.context_token = None

    async def __aenter__(self):
        self.context_token = _session_context.set(_SessionMaker())
        return type(self)

    async def __aexit__(self, exc_type, exc_value, traceback):
        _session = _session_context.get()
        if exc_type is not None:
           await  _session.rollback()

        await _session.commit()
        await _session.close()

        _session_context.reset(self.context_token)


def get_session() -> AsyncSession:
    _session = _session_context.get()
    if _session is None:
        raise Exception('There is no Session in the current context')

    return _session


class SessionMeta(type):
    def __getattr__(self, key):
        return getattr(get_session(), key)


class _Session(metaclass=SessionMeta):
    pass


Session: AsyncSession = _Session