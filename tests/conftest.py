import pytest
import pytest_asyncio
import asyncio
import os

from src.schemas.user_schemas import (
    HashedUserSchema,
    UserAuthSchema,
    UserRegisterSchema,
    LoggedUserSchema,
)
from src.schemas.event_schemas import NoIdsEventSchema
from src.models.sql_models import Base, UsersOrm, EventStatus

skip_in_ci = pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipping in CI")


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
    from src.utils.session import async_session

    async with async_session() as session:
        yield session


@pytest_asyncio.fixture()
async def create_tables():
    from src.utils.session import async_engine

    print("Creating tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tables created successfully")
    await async_engine.dispose()
    yield


@pytest.fixture
def users():
    from src.utils.auth_utils import hash_password

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
def user_register():
    user = UserRegisterSchema(
        email="testmail@test.com",
        username="Slava",
        password="secretpass",
        active_status=True,
    )
    return user


@pytest.fixture
def user_auth():
    user = UserAuthSchema(
        email="testmail@test.com",
        password="secretpass",
        active_status=True,
    )
    return user


@pytest.fixture
def user_orm():
    from src.utils.auth_utils import hash_password

    pass1 = hash_password("secretpass")
    user = UsersOrm(
        id=1,
        email="testmail@test.com",
        username="Slava",
        password=pass1,
        user_status=True,
    )
    return user


@pytest.fixture
def user_logged():
    return LoggedUserSchema(
        email="testmail@test.com", username="Slava", active_status=True, id=1
    )


@pytest.fixture
def no_id_events():
    return [
        NoIdsEventSchema(
            user_id=1,
            name="first_event",
            description="rk0gr0gk rgkr0gkg rkgr",
            event_status=EventStatus.FUTURE,
            parent_id=2,
        ),
        NoIdsEventSchema(
            user_id=1,
            name="second_event",
            description="rk0gr0gk rgkr0gkg rkgr",
            event_status="current",
            parent_id=4,
        ),
        NoIdsEventSchema(
            user_id=1,
            name="third_event",
            description="rk0gr0gk rgkr0gkg rkgr",
            event_status=EventStatus.PAST,
            parent_id=4,
        ),
    ]
