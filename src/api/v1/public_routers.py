from fastapi import APIRouter, Depends, Query

from src.services.public_service import PublicService
from src.utils.dependencies import get_public_service

router = APIRouter(tags=["Публичное", "Пользователи"])


@router.get("/users")
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: PublicService = Depends(get_public_service),
):
    res = await service.get_users_paginated(limit=limit, skip=skip)
    return res


@router.get("/users/{user_id}")
async def get_user_by_id(
    user_id: int, service: PublicService = Depends(get_public_service)
):
    user_info = await service.get_user_info(user_id)
    return user_info
