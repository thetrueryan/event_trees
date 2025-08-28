from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.sql_models import UsersOrm


class EventsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
