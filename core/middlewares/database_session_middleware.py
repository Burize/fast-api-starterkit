from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker


from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request

from core.database.session import session_context
from core.inject import injector


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        async with DBSessionContext():
            response = await call_next(request)
        return response


class DBSessionContext:
    def __init__(self):
        self.context_token = None
        self._engine = injector.get(Engine)

    async def __aenter__(self):
        session_maker = async_sessionmaker(self._engine, expire_on_commit=False)
        self.context_token = session_context.set(session_maker())
        return type(self)

    async def __aexit__(self, exc_type, exc_value, traceback):
        _session = session_context.get()
        if exc_type is not None:
            await _session.rollback()

        await _session.commit()
        await _session.close()

        session_context.reset(self.context_token)
