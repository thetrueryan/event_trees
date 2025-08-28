import pytest
import pytest_asyncio

from src.repositories.users_repo import UsersRepository
from src.core.config import settings
from src.models.sql_models import UsersOrm


@pytest.mark.asyncio
async def test_add_and_get_users(users, test_session):
    assert settings.MODE == "TEST"
    repo = UsersRepository(test_session)
    for user in users:
        uid = await repo.add_one(user)
        assert isinstance(uid, int)
        user = await repo.get_one(user_email=user.email)
        assert isinstance(user, UsersOrm)
