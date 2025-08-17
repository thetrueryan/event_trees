from fastapi import APIRouter

from schemas.user_schemas import UserAuthSchema



router = APIRouter(
    tags=["Аутентификация"]
)


@router.post("/register")
async def register_user(
    user: UserAuthSchema,
):
    pass