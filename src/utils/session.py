from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import create_engine

from src.core.config import DB_ASYNC_URL

async_engine = create_async_engine(
    url=DB_ASYNC_URL,
    echo=False,
    pool_pre_ping=True,
)
sync_engine = create_engine(
    url=DB_ASYNC_URL,
    echo=False,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(async_engine)
