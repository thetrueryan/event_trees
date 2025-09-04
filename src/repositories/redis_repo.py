from redis.asyncio import Redis

from src.core.logger import logger
from src.schemas.event_schemas import EventSchema


class RedisRepository:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def _cache_event_key(self, user_id: int, event_local_id: int) -> str:
        return f"user:{user_id}:event:{event_local_id}"

    async def add_one(self, event: EventSchema, ttl: int = 3600) -> None:
        try:
            key = self._cache_event_key(event.user_id, event.local_id)
            await self.redis.setex(name=key, time=ttl, value=event.model_dump_json())
        except Exception as e:
            logger.error(f"Cannot cash in redis: {e}")
        return None
