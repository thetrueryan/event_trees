from fastapi import HTTPException, status

from sqlalchemy.exc import SQLAlchemyError
from src.models.sql_models import EventStatus
from src.repositories.events_repo import EventsRepository
from src.schemas.event_schemas import EventSchema, NoIdsEventSchema, LocalIdEventSchema
from src.schemas.user_schemas import LoggedUserSchema
from src.core.logger import logger
from src.utils.excepts import unknown_error, not_found_error


class EventsService:
    def __init__(self, events_repository: EventsRepository):
        self.events_repository = events_repository

    async def get_events(self, user: LoggedUserSchema) -> list[EventSchema] | None:
        """
        Get every events by user id
        """
        events = await self.events_repository.get_all(user.id)
        return events

    async def add_event(
        self, user: LoggedUserSchema, event_no_id: NoIdsEventSchema
    ) -> EventSchema | None:
        """
        add event buisness logic
        """
        try:
            max_event_local_id = await self.events_repository.get_max_local_id(user.id)
            if not max_event_local_id:
                new_local_id = 1
            else:
                new_local_id = max_event_local_id + 1
            if event_no_id.parent_id:
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
            if event_id:
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
        return None

    async def get_event_by_id(
        self, user: LoggedUserSchema, event_local_id: int
    ) -> EventSchema | None:
        try:
            event = await self.events_repository.get_event_by_local_id(
                user_id=user.id, local_id=event_local_id
            )
            if not event:
                raise not_found_error
            return event
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error: {e}")
            raise unknown_error

    async def delete_event_by_local_id(
        self, user: LoggedUserSchema, event_local_id: int
    ) -> bool:
        event_to_delete = await self.events_repository.get_event_by_local_id(
            user_id=user.id, local_id=event_local_id
        )
        if not event_to_delete:
            raise not_found_error
        child_events = await self.events_repository.get_events_by_parent_id(
            user_id=user.id,
            parent_id=event_to_delete.local_id,
        )
        if child_events:
            child_status = True
        else:
            child_status = False

        delete_status = await self.events_repository.delete_one(
            event_to_delete=event_to_delete,
            child_events=child_status,
        )
        return delete_status
