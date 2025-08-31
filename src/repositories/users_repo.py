from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_schemas import HashedUserSchema, ToPublicUserSchema
from src.models.sql_models import UsersOrm
from src.utils.events_utils import events_from_orm_to_schema
from src.utils.public_utils import from_user_orm_to_public_user


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

    async def get_one_with_relationship(
        self, user_id: int
    ) -> ToPublicUserSchema | None:
        stmt = (
            select(UsersOrm)
            .options(selectinload(UsersOrm.events))
            .where(UsersOrm.id == user_id)
        )
        res = await self.session.execute(stmt)
        user = res.scalar_one_or_none()
        if user:
            return from_user_orm_to_public_user(user)
        return None

    async def get_all_with_relationship_paginated(
        self, limit: int, skip: int
    ) -> list[ToPublicUserSchema]:
        stmt = (
            select(UsersOrm)
            .options(selectinload(UsersOrm.events))
            .order_by(UsersOrm.id)
            .offset(skip)
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        users = res.scalars().all()
        return [from_user_orm_to_public_user(user) for user in users]
