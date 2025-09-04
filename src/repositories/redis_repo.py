from redis.asyncio import Redis

from src.core.logger import logger
from src.schemas.event_schemas import EventSchema


class RedisRepository:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def _cache_event_key(self, event_id: int) -> str:
        return f"event:{event_id}"

    async def add_one(self, event: EventSchema) -> None:
        try:
            key = self._cache_event_key(event.id)
            await self.redis.setex(name=key, time=3600, value=event.model_dump_json())
        except Exception as e:
            logger.error(f"Cannot cash in redis: {e}")
        return None
