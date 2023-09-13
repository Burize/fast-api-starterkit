from fastapi import Depends

from .redis_session_storage import RedisSessionStorage
from ..storages import RedisStorage


def get_session_storage():
    redis_storage = RedisStorage()
    redis_session_storage = RedisSessionStorage(redis_storage=redis_storage)
    return redis_session_storage
