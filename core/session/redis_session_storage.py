from typing import Optional
from uuid import UUID
import core.settings as settings

from core.storages import RedisStorage
from .session_storage import SessionStorage
from ..inject import inject



class RedisSessionStorage(SessionStorage):
    @inject
    def __init__(self, redis_storage: RedisStorage):
        self._redis_storage = redis_storage

    def create_session(self, user_id: UUID, session_id: str):
        self._redis_storage.set(f'user:{user_id.hex}', session_id)
        self._redis_storage.set(f'session:{session_id}', user_id.hex, expire=settings.USER_SESSION_MAX_AGE)

    def prolong_session(self, session_id: str):
        self._redis_storage.expire(f'session:{session_id}', expire=settings.USER_SESSION_MAX_AGE)

    def get_user_id(self, session_id: str) -> Optional[UUID]:
        user_id =  self._redis_storage.get(f'session:{session_id}')
        return user_id and UUID(user_id)

    def get_user_active_session_id(self, user_id: UUID) -> Optional[str]:
        return self._redis_storage.get(f'user:{user_id.hex}')

    def delete_session(self, user_id: UUID):
        session_id = self._redis_storage.get(f'user:{user_id.hex}')
        self._redis_storage.delete(f'user:{user_id.hex}')
        if session_id:
            self._redis_storage.delete(f'session:{session_id}')
