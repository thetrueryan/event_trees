from fastapi import APIRouter, Depends

from src.services.profile_service import ProfileService
from src.services.events_service import EventsService
from src.schemas.user_schemas import LoggedUserSchema
from src.utils.dependencies import (
    get_current_auth_user,
    get_profile_service,
    get_events_service,
)

router = APIRouter(tags=["Пользователь", "Профиль"])


@router.get("/user")
async def user_info(user: LoggedUserSchema = Depends(get_current_auth_user)):
    return user.model_dump()


@router.get("/user/profile")
async def user_profile(
    user: LoggedUserSchema = Depends(get_current_auth_user),
    service: EventsService = Depends(get_events_service),
):
    user_events_data = await service.get_user_events_data(user)
    return {
        "user": user,
        "data": user_events_data,
    }
