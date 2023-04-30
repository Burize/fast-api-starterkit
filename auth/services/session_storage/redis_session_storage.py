from typing import Awaitable
from uuid import uuid4

from fastapi import Depends

from core.storages import RedisStorage
from .session_storage import SessionId
from .session_storage import SessionStorage


class RedisSessionStorage(SessionStorage):
    def __init__(self, redis_storage: RedisStorage = Depends()):
        self._redis_storage = redis_storage

    async def create_session(self, data: dict) -> SessionId:
        session_id = uuid4()
        await self._redis_storage.set(session_id, data)
        return session_id

    async def get_session(self, session_id: SessionId) -> dict:
        return await self._redis_storage.get(session_id)

    async def delete_session(self, session_id: SessionId):
        await self._redis_storage.delete(session_id)
