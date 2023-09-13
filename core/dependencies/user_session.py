from typing import Annotated
from typing import Optional
from fastapi import  Cookie
from fastapi import  Response
from fastapi import  Depends

from core import settings
from core.session import SessionStorage
from core.session import get_session_storage


async def prolong_session(
    session_storage: Annotated[SessionStorage, Depends(get_session_storage)],
    response: Response,
    session_id: Annotated[Optional[str], Cookie()] = None,
):
    if not session_id:
        return

    await session_storage.prolong_session(session_id)
    response.set_cookie(key=settings.USER_SESSION_NAME, max_age=settings.USER_SESSION_MAX_AGE, value=session_id)

