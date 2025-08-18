from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user_schemas import LoggedUserSchema
from models.sql_models import UsersOrm
from repositories.abstract_repo import AbstractRepository


class UsersRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, user: dict) -> int:
        stmt = insert(UsersOrm).values(**user).returning(UsersOrm.id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar_one_or_none()

    async def get_one(self, user_id: int) -> UsersOrm:
        stmt = (
            select(UsersOrm)
            .where(UsersOrm.id == user_id)
            .options(selectinload(UsersOrm.events))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
