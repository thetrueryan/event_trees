from fastapi import APIRouter, Depends, HTTPException, status

from schemas.other_schemas import TokenInfo
from schemas.user_schemas import UserAuthSchema
from utils.dependencies import get_auth_service
from services.auth_service import AuthService
from core.logger import logger
from utils.excepts import unknown_error

router = APIRouter(tags=["Аутентификация"])


@router.post(
    "/register",
    response_model=TokenInfo,
    status_code=status.HTTP_201_CREATED,
    summary="регистрация нового пользователя",
)
async def register(
    user: UserAuthSchema,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        registered_user = await auth_service.register_user(user)
        access_token = await auth_service.create_access_token(registered_user)
        refresh_token = await auth_service.create_refresh_token(registered_user)
        return TokenInfo(access_token, refresh_token)
    except Exception as e:
        logger.error(f"Unknown ERROR: {e}")
        raise unknown_error


@router.post(
    "/login", response_model=TokenInfo, summary="регистрация нового пользователя"
)
async def login(
    user: UserAuthSchema,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        logged_user = await auth_service.login_user(user)
        access_token = await auth_service.create_access_token(logged_user)
        refresh_token = await auth_service.create_refresh_token(logged_user)
        return TokenInfo(access_token, refresh_token)
    except Exception as e:
        logger.error(f"Unknown ERROR: {e}")
        raise unknown_error
