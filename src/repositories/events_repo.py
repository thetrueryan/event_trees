from sqlalchemy import select, insert, func, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.event_schemas import EventSchema, NoIdsEventSchema, LocalIdEventSchema
from src.models.sql_models import EventsOrm
from src.utils.events_utils import events_from_orm_to_schema
from src.core.logger import logger


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
            event_status=event.event_status,
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

    async def get_event_by_local_id(
        self, user_id: int, local_id: int
    ) -> EventSchema | None:
        stmt = select(EventsOrm).where(
            EventsOrm.user_id == user_id, EventsOrm.local_id == local_id
        )
        res = await self.session.execute(stmt)
        event = res.scalar_one_or_none()
        if event:
            return events_from_orm_to_schema(event)
        return None

    async def get_events_by_parent_id(
        self,
        user_id: int,
        parent_id: int,
    ) -> list[EventSchema] | None:
        stmt = select(EventsOrm).where(
            EventsOrm.user_id == user_id, EventsOrm.parent_id == parent_id
        )
        res = await self.session.execute(stmt)
        events = res.scalars().all()
        if events:
            return [events_from_orm_to_schema(event) for event in events]
        return None

    async def delete_one(
        self,
        event_to_delete: EventSchema,
        child_events: bool,
    ) -> bool:
        try:
            if child_events:
                child_stmt = (
                    update(EventsOrm)
                    .where(
                        EventsOrm.user_id == event_to_delete.user_id,
                        EventsOrm.parent_id == event_to_delete.local_id,
                    )
                    .values(parent_id=event_to_delete.parent_id)
                )
                await self.session.execute(child_stmt)
                await self.session.flush()
            delete_stmt = delete(EventsOrm).where(
                EventsOrm.user_id == event_to_delete.user_id,
                EventsOrm.id == event_to_delete.id,
            )
            await self.session.execute(delete_stmt)
            await self.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error while deleting EventsOrm: {e}")
            return False
