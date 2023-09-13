from typing import Optional
from uuid import UUID
from core import settings

from core.storages import RedisStorage
from .session_storage import SessionStorage
from ..inject import inject


class RedisSessionStorage(SessionStorage):
    @inject
    def __init__(self, redis_storage: RedisStorage):
        self._redis_storage = redis_storage

    async def create_session(self, user_id: UUID, session_id: str):
        await self._redis_storage.set(f'user:{user_id.hex}', session_id)
        await self._redis_storage.set(f'session:{session_id}', user_id.hex, expire=settings.USER_SESSION_MAX_AGE)

    async def prolong_session(self, session_id: str):
        await self._redis_storage.expire(f'session:{session_id}', expire=settings.USER_SESSION_MAX_AGE)

    async def get_user_id(self, session_id: str) -> Optional[UUID]:
        user_id = await self._redis_storage.get(f'session:{session_id}')
        return user_id and UUID(user_id)

    async def get_user_active_session_id(self, user_id: UUID) -> Optional[str]:
        return await self._redis_storage.get(f'user:{user_id.hex}')

    async def delete_session(self, user_id: UUID):
        session_id = await self._redis_storage.get(f'user:{user_id.hex}')
        await self._redis_storage.delete(f'user:{user_id.hex}')
        if session_id:
            await self._redis_storage.delete(f'session:{session_id}')
