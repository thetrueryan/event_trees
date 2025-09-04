from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import InvalidTokenError
from redis.asyncio import Redis

from src.utils import redis_module
from src.core.logger import logger
from src.repositories.users_repo import UsersRepository
from src.repositories.events_repo import EventsRepository
from src.repositories.redis_repo import RedisRepository
from src.utils.session import async_session
from src.utils.auth_utils import decode_jwt, logged_schema_from_orm
from src.services.auth_service import AuthService
from src.services.events_service import EventsService
from src.services.profile_service import ProfileService
from src.services.public_service import PublicService


# redis
async def get_redis_client() -> Redis | None:
    return redis_module.redis


# session
async def get_session():
    async with async_session() as session:
        yield session


# repositories (SQL)
def get_users_repository(session: AsyncSession = Depends(get_session)):
    return UsersRepository(session)


def get_events_repository(session: AsyncSession = Depends(get_session)):
    return EventsRepository(session)


# repositories (Redis)
def get_redis_repository(redis: Redis = Depends(get_redis_client)):
    return RedisRepository(redis)


# services
def get_auth_service(
    repo: UsersRepository = Depends(get_users_repository),
) -> AuthService:
    return AuthService(repo)


def get_events_service(
    sql_repo: EventsRepository = Depends(get_events_repository),
    redis_repo: Redis = Depends(get_redis_repository),
) -> EventsService:
    return EventsService(events_repository=sql_repo, redis_repository=redis_repo)


def get_profile_service(
    repo: UsersRepository = Depends(get_users_repository),
) -> ProfileService:
    return ProfileService(repo)


def get_public_service(
    repo: UsersRepository = Depends(get_users_repository),
) -> PublicService:
    return PublicService(repo)


# oauth2passwordbearer & httpbearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="Bearer")

http_bearer = HTTPBearer(auto_error=False)


# auth dependencies
async def get_current_token_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        logger.error(f"Error in token payload: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error"
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    auth_service: AuthService = Depends(get_auth_service),
):
    token_type = payload.get("type")
    if token_type != "access":
        logger.error(f"Invalid token_type: {token_type}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type: {token_type}",
        )

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error"
        )
    user_id = int(user_id_str)
    user = await auth_service.users_repository.get_one(user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return logged_schema_from_orm(user)


async def get_current_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
    auth_service: AuthService = Depends(get_auth_service),
):
    token_type = payload.get("type")
    if token_type != "refresh":
        logger.error(f"Invalid token_type: {token_type}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type: {token_type}",
        )
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error"
        )
    user_id = int(user_id_str)
    user = await auth_service.users_repository.get_one(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return logged_schema_from_orm(user)
