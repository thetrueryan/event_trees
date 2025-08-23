import pytest
import pytest_asyncio
import asyncio

from src.utils.session import async_engine, sync_engine, async_session
from src.schemas.user_schemas import HashedUserSchema, UserAuthSchema
from src.utils.auth_utils import hash_password
from src.models.sql_models import Base, UsersOrm, EventsOrm


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_session():
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables():
    print("Creating tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tables created successfully")
    await async_engine.dispose()
    yield


@pytest.fixture
def users():
    pass1 = hash_password("secretpass")
    pass2 = hash_password("qwerty123")

    users = [
        HashedUserSchema(
            email="testmail@test.com",
            username="Slava",
            password=pass1,
        ),
        HashedUserSchema(
            email="qwertymail@qwerty.com",
            username="Lesha",
            password=pass2,
        ),
    ]
    return users


@pytest.fixture
def user_auth():
    user = UserAuthSchema(
        email="testmail@test.com",
        username="Slava",
        password="secretpass",
    )
    return user
