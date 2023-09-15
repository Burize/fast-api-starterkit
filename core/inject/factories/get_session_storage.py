from core.session.redis_session_storage import RedisSessionStorage
from core.storages import RedisStorage


def get_session_storage():
    redis_storage = RedisStorage()
    redis_session_storage = RedisSessionStorage(redis_storage=redis_storage)
    return redis_session_storage
