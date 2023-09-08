from typing import Optional
from uuid import UUID

from fastapi import Request
UserId = UUID

async def get_user_id(request: Request) -> Optional[UserId]:
    try:
        return request.state.user_id
    except:
        return None
