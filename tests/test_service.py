import pytest
import pytest_asyncio

from src.services.auth_service import AuthService
from src.repositories.users_repo import UsersRepository
from src.utils.dependencies import get_auth_service
from src.schemas.user_schemas import LoggedUserSchema


@pytest.mark.asyncio
async def test_register(user_auth):
    service = get_auth_service()
    assert isinstance(service, AuthService)

    user = await service.register_user(user_auth)
    assert isinstance(user, LoggedUserSchema)
