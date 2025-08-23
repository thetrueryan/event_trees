from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_schemas import HashedUserSchema
from src.models.sql_models import UsersOrm
from src.repositories.abstract_repo import AbstractRepository


class UsersRepository(AbstractRepository):
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

    async def get_one(self, user_id: int) -> UsersOrm:
        stmt = (
            select(UsersOrm)
            .where(UsersOrm.id == user_id)
            .options(selectinload(UsersOrm.events))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
