from fastapi import APIRouter, Depends

from src.services.public_service import PublicService
from src.utils.dependencies import get_public_service

router = APIRouter(tags=["Публичное", "Пользователи"])


@router.get("/users")
async def get_all_users():
    pass


@router.get("/users/{user_id}")
async def get_user_by_id(
    user_id: int, service: PublicService = Depends(get_public_service)
):
    user_info = await service.get_user_info(user_id)
    return user_info
