from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

from core import settings
from core.inject import injector
from core.session import SessionStorage


class UserSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        response = await call_next(request)

        session_id = request.cookies.get('session_id', None)
        user_id = getattr(request.state, 'user_id', None)
        is_logout = 'logout' in request.url.path
        if is_logout or not session_id or not user_id:
            return response

        session_storage = injector.get(SessionStorage)
        await session_storage.prolong_session(session_id)
        response.set_cookie(key=settings.USER_SESSION_NAME, max_age=settings.USER_SESSION_MAX_AGE, value=session_id)
        return response
