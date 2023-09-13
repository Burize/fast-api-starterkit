from fastapi import Depends

from .redis_session_storage import RedisSessionStorage


async def get_session_storage(redis_session_storage: RedisSessionStorage = Depends()):
    return redis_session_storage
