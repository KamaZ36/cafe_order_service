from redis.asyncio import Redis


class RedisRateLimiter:
    def __init__(self, redis_client: Redis) -> None:
        self._redis = redis_client

    async def hit(self, key: str, limit: int, window_seconds: int) -> bool:
        """Увеличивает счётчик по ключу и возвращает True, если лимит не превышен."""

        current = await self._redis.incr(key)

        if current == 1:
            await self._redis.expire(key, window_seconds)

        return current <= limit
