from sqlalchemy import select, insert, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.event_schemas import EventSchema, NoIdsEventSchema, LocalIdEventSchema
from src.models.sql_models import EventsOrm
from src.utils.events_utils import events_from_orm_to_schema


class EventsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, user_id: int) -> list[EventSchema] | None:
        stmt = (
            select(EventsOrm)
            .where(EventsOrm.user_id == user_id)
            .order_by(EventsOrm.local_id.asc())
        )
        res = await self.session.execute(stmt)
        events = res.scalars().all()
        if events:
            return [events_from_orm_to_schema(event) for event in events]
        return None

    async def add_one(self, event: LocalIdEventSchema) -> int | None:
        new_event = EventsOrm(
            user_id=event.user_id,
            local_id=event.local_id,
            parent_id=event.parent_id,
            name=event.name,
            description=event.description,
        )
        self.session.add(new_event)
        await self.session.flush()
        event_id = new_event.id
        await self.session.commit()
        return event_id

    async def get_max_local_id(self, user_id: int) -> int | None:
        stmt = select(func.max(EventsOrm.local_id)).where(EventsOrm.user_id == user_id)
        res = await self.session.execute(stmt)
        return res.scalar()
