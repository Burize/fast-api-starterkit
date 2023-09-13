from typing import Annotated
from typing import Optional
from fastapi import Cookie
from fastapi import Request

from core.exceptions import NotAuthorizedException
from core.inject import injector
from core.session import SessionStorage


async def authorize(
    request: Request,
    session_id: Annotated[Optional[str], Cookie()] = None,
):
    session_storage = injector.get(SessionStorage)

    if not session_id:
        raise NotAuthorizedException()

    user_id = await session_storage.get_user_id(session_id)
    if not user_id:
        raise NotAuthorizedException()

    active_session_id = await session_storage.get_user_active_session_id(user_id)

    if session_id != active_session_id:
        raise NotAuthorizedException()

    request.state.user_id = user_id
