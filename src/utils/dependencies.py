from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import InvalidTokenError

from src.core.logger import logger
from src.repositories.users_repo import UsersRepository
from src.repositories.events_repo import EventsRepository
from src.utils.session import async_session
from src.utils.auth_utils import decode_jwt, logged_schema_from_orm
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
def get_auth_service(
    repo: UsersRepository = Depends(get_users_repository),
) -> AuthService:
    return AuthService(repo)


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
