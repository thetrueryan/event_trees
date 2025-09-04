from fastapi import FastAPI
import uvicorn
from redis.asyncio import Redis
from contextlib import asynccontextmanager

from src.core.config import REDIS_URL
from src.utils import redis_module
from src.api.v1.auth_routers import router as auth_router
from src.api.v1.profile_routers import router as profile_router
from src.api.v1.events_routers import router as event_router
from src.api.v1.public_routers import router as public_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_module.redis = Redis.from_url(url=REDIS_URL, decode_responses=True)
    yield
    await redis_module.redis.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(event_router)
app.include_router(public_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
