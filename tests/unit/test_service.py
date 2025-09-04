import pytest
import pytest_asyncio
from unittest.mock import AsyncMock

from src.services.auth_service import AuthService
from src.services.events_service import EventsService
from src.repositories.users_repo import UsersRepository
from src.repositories.events_repo import EventsRepository
from src.repositories.redis_repo import RedisRepository
from src.schemas.user_schemas import LoggedUserSchema
from src.schemas.event_schemas import EventSchema
from src.models.sql_models import UsersOrm, EventsOrm


@pytest.mark.asyncio
async def test_register(user_register):
    mock_repo = AsyncMock(spec=UsersRepository)
    mock_repo.add_one.return_value = 1

    service = AuthService(mock_repo)
    user = await service.register_user(user_register)

    assert isinstance(user, LoggedUserSchema)
    assert user.email == user_register.email
    assert user.username == user_register.username
    assert user.id == 1


@pytest.mark.asyncio
async def test_login(user_auth, user_orm):
    mock_repo = AsyncMock(spec=UsersRepository)
    mock_repo.get_one.return_value = user_orm

    service = AuthService(mock_repo)
    user = await service.login_user(user_auth)

    assert isinstance(user, LoggedUserSchema)
    assert user.email == user_auth.email
    assert user.id == 1


@pytest.mark.asyncio
async def test_add_event(user_logged, no_id_events):
    mock_repo = AsyncMock(spec=EventsRepository)
    mock_redis = AsyncMock(spec=RedisRepository)
    mock_repo.get_local_ids.return_value = [2, 4]
    mock_repo.add_one.return_value = 5
    service = EventsService(mock_repo, mock_redis)
    for no_id_event in no_id_events:
        event = await service.add_event(user=user_logged, event_no_id=no_id_event)
        assert isinstance(event, EventSchema)
        assert event.local_id > event.parent_id
        mock_repo.get_local_ids.return_value.append(event.local_id)
