from typing import Optional
from typing import Union
from uuid import UUID

import redis


RedisKey = Union[str, int, UUID]
RedisValue = Union[dict, set, str, UUID, int]


class RedisStorage:
    def __init__(self):
        self._redis = redis.Redis(decode_responses=True)

    def get(self, key: RedisKey) -> RedisValue:
        return self._redis.get(key)

    def set(self, key: RedisKey, value: RedisValue, expire: Optional[int] = None):
        self._redis.set(key, value, ex=expire)

    def expire(self, key: RedisKey, expire: int):
        self._redis.expire(key, expire)

    def delete(self, key: RedisKey):
        self._redis.delete(key)
