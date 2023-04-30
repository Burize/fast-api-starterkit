from typing import Union
from uuid import UUID

import redis.asyncio as _redis


RedisKey = Union[str, int, UUID]
RedisValue = Union[dict, set, str, UUID, int]


class RedisStorage:
    def __init__(self):
        self._redis = _redis.Redis()

    async def set(self, key: RedisKey, value: RedisValue):
        await self._redis.set(key, value)

    async def delete(self, key: RedisKey):
        await self._redis.delete(key)

    async def get(self, key: RedisKey) -> RedisValue:
        return self._redis.get(key)






