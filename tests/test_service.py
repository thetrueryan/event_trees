import pytest
import pytest_asyncio
from unittest.mock import AsyncMock

from src.services.auth_service import AuthService
from src.repositories.users_repo import UsersRepository
from src.utils.dependencies import get_auth_service
from src.schemas.user_schemas import LoggedUserSchema
from src.models.sql_models import UsersOrm


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
