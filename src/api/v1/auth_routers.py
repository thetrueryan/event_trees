from fastapi import APIRouter, Depends

from schemas.other_schemas import TokenInfo
from schemas.user_schemas import UserAuthSchema
from utils.dependencies import get_auth_service
from services.auth_service import AuthService

router = APIRouter(
    tags=["Аутентификация"]
)


@router.post(
        "/register",
        response_model=TokenInfo
        )
async def register_user(
    user: UserAuthSchema,
    auth_service: AuthService = Depends(get_auth_service),
):
    registered_user = await auth_service.register_user(user)
    if registered_user:
        access_token = await auth_service.create_access_token(registered_user)
        refresh_token = await auth_service.create_refresh_token(registered_user)
    
    return TokenInfo(access_token, refresh_token)