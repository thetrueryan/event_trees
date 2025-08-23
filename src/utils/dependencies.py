from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users_repo import UsersRepository
from src.repositories.events_repo import EventsRepository
from src.utils.session import async_session
from src.services.auth_service import AuthService


# session
async def get_session():
    async with async_session() as session:
        yield session


# repositories
def get_users_repository(session: AsyncSession = Depends(get_session)):
    return UsersRepository(session)


def get_events_repository(session: AsyncSession = Depends(get_session)):
    return EventsRepository(session)


# services
def get_auth_service(repo: UsersRepository = Depends(get_users_repository)):
    return AuthService(repo)
