from redis.asyncio import Redis

from src.core.logger import logger
from src.schemas.event_schemas import EventSchema


class RedisRepository:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def _cache_event_key(self, user_id: int, event_local_id: int) -> str:
        return f"user:{user_id}:event:{event_local_id}"

    async def set_one(self, event: EventSchema, ttl: int = 3600) -> None:
        try:
            key = self._cache_event_key(event.user_id, event.local_id)
            await self.redis.setex(name=key, time=ttl, value=event.model_dump_json())
        except Exception as e:
            logger.error(f"Cannot cash in redis: {e}")
        return None

    async def get_one(self, user_id: int, local_id: int) -> EventSchema | None:
        try:
            key = self._cache_event_key(user_id, local_id)
            cached_event = await self.redis.get(key)
            if not cached_event:
                return None
            return EventSchema.model_validate_json(cached_event)
        except Exception as e:
            logger.error(f"Failed to get event from cache: {e}")
            await self.delete_one(user_id, local_id)
            return None

    async def delete_one(self, user_id: int, local_id: int) -> bool:
        try:
            key = self._cache_event_key(user_id, local_id)
            result = await self.redis.delete(key)
            return bool(result)
        except Exception as e:
            logger.error(f"Failed to delete event from cache: {e}")
            return False
