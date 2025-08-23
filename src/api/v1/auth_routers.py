from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.other_schemas import TokenInfo
from src.schemas.user_schemas import UserAuthSchema
from src.utils.dependencies import get_auth_service
from src.services.auth_service import AuthService
from src.core.logger import logger
from src.utils.excepts import unknown_error

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
    registered_user = await auth_service.register_user(user)
    access_token = await auth_service.create_access_token(registered_user)
    refresh_token = await auth_service.create_refresh_token(registered_user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/login", response_model=TokenInfo, summary="регистрация нового пользователя"
)
async def login(
    user: UserAuthSchema,
    auth_service: AuthService = Depends(get_auth_service),
):
    logged_user = await auth_service.login_user(user)
    access_token = await auth_service.create_access_token(logged_user)
    refresh_token = await auth_service.create_refresh_token(logged_user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)
