from fastapi import APIRouter, Depends

from src.schemas.user_schemas import LoggedUserSchema
from src.utils.dependencies import get_current_auth_user

router = APIRouter(tags=["Пользователь"])


@router.get("/user")
async def user_info(user: LoggedUserSchema = Depends(get_current_auth_user)):
    return {
        "username": user.username,
        "email": user.email,
    }
