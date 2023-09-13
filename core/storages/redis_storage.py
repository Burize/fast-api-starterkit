from typing import Optional
from typing import Union
from uuid import UUID

import redis.asyncio as redis


RedisKey = Union[str, int, UUID]
RedisValue = Union[dict, set, str, UUID, int]


class RedisStorage:
    def __init__(self):
        self._redis = redis.Redis(decode_responses=True)

    async def get(self, key: RedisKey) -> RedisValue:
        return await self._redis.get(key)

    async def set(self, key: RedisKey, value: RedisValue, expire: Optional[int] = None):
        await self._redis.set(key, value, ex=expire)

    async def expire(self, key: RedisKey, expire: int):
        await self._redis.expire(key, expire)

    async def delete(self, key: RedisKey):
        await self._redis.delete(key)
