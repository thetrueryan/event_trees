from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_schemas import HashedUserSchema
from src.models.sql_models import UsersOrm


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, user: HashedUserSchema) -> int:
        new_user = UsersOrm(
            username=user.username,
            email=user.email,
            password=user.password,
            user_status=user.active_status,
        )
        self.session.add(new_user)
        await self.session.flush()
        user_id = new_user.id
        await self.session.commit()
        return user_id

    async def get_one(
        self, user_id: int | None = None, user_email: str | None = None
    ) -> UsersOrm | None:
        if not user_id and not user_email:
            return None

        if user_id:
            stmt = select(UsersOrm).where(UsersOrm.id == user_id)

        if user_email:
            stmt = select(UsersOrm).where(UsersOrm.email == user_email)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
