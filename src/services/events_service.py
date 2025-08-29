from fastapi import HTTPException, status

from src.models.sql_models import EventStatus
from src.repositories.events_repo import EventsRepository
from src.schemas.event_schemas import EventSchema, NoIdsEventSchema, LocalIdEventSchema
from src.schemas.user_schemas import LoggedUserSchema
from src.core.logger import logger
from src.utils.excepts import unknown_error


class EventsService:
    def __init__(self, events_repository: EventsRepository):
        self.events_repository = events_repository

    async def get_events(self, user: LoggedUserSchema) -> list[EventSchema] | None:
        events = await self.events_repository.get_all(user.id)
        return events

    async def add_event(
        self, user: LoggedUserSchema, event_no_id: NoIdsEventSchema
    ) -> EventSchema:
        try:
            max_event_local_id = await self.events_repository.get_max_local_id(user.id)
            if not max_event_local_id:
                new_local_id = 1
            else:
                new_local_id = max_event_local_id + 1

            if event_no_id.parent_id > new_local_id:
                raise ValueError(
                    f"parent event not create (id: {event_no_id.parent_id})"
                )
            event = LocalIdEventSchema(
                user_id=event_no_id.user_id,
                name=event_no_id.name,
                description=event_no_id.description,
                event_status=event_no_id.event_status,
                parent_id=event_no_id.parent_id,
                local_id=new_local_id,
            )
            event_id = await self.events_repository.add_one(event)
            return EventSchema(
                user_id=event.user_id,
                name=event.name,
                description=event.description,
                event_status=event_no_id.event_status,
                parent_id=event.parent_id,
                local_id=event.local_id,
                id=event_id,
            )
        except ValueError as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="parent event not create",
            )
        except Exception as e:
            logger.error(f"Unknown error: {e}")
            raise unknown_error
