from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.sql_models import UsersOrm
from src.repositories.abstract_repo import AbstractRepository


class EventsRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
