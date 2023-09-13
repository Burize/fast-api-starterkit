from typing import Optional
from uuid import UUID

from fastapi import Depends
from fastapi import Request


async def _get_user_id(request: Request) -> Optional[UUID]:
    try:
        return request.state.user_id
    except:
        return None


get_user_id = Depends(_get_user_id)
