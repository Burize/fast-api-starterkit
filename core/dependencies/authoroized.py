from typing import Annotated
from typing import Optional
from fastapi import  Cookie
from fastapi import  Request
from fastapi import  Depends

from core.exceptions import NotAuthorizedException
from core.session import SessionStorage
from core.session import get_session_storage


def authorized(
    session_storage: Annotated[SessionStorage, Depends(get_session_storage)],
    request: Request,
    session_id: Annotated[Optional[str], Cookie()] = None,
):
    if not session_id:
        raise NotAuthorizedException()

    user_id = session_storage.get_user_id(session_id)
    if not user_id:
        raise NotAuthorizedException()

    active_session_id = session_storage.get_user_active_session_id(user_id)

    if session_id != active_session_id:
        raise NotAuthorizedException()

    request.state.user_id = user_id
