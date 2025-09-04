from fastapi import HTTPException, status

from sqlalchemy.exc import SQLAlchemyError
from src.models.sql_models import EventStatus
from src.repositories.events_repo import EventsRepository
from src.repositories.redis_repo import RedisRepository
from src.schemas.event_schemas import (
    EventSchema,
    NoIdsEventSchema,
    LocalIdEventSchema,
    EventToUpdateSchema,
    UserIdEventSchema,
)
from src.schemas.user_schemas import LoggedUserSchema
from src.core.logger import logger
from src.utils.excepts import unknown_error, not_found_error


class EventsService:
    def __init__(
        self, events_repository: EventsRepository, redis_repository: RedisRepository
    ):
        self.events_repository = events_repository
        self.redis_repository = redis_repository

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
            local_ids = await self.events_repository.get_local_ids(user.id)
            if not local_ids:
                new_local_id = 1
            else:
                max_local_id = max(local_ids)
                new_local_id = max_local_id + 1
            if event_no_id.parent_id:
                if (
                    event_no_id.parent_id > new_local_id
                    or event_no_id.parent_id not in local_ids
                ):
                    raise ValueError(
                        f"parent event not create (id: {event_no_id.parent_id})"
                    )
            event = LocalIdEventSchema(
                user_id=user.id,
                name=event_no_id.name,
                description=event_no_id.description,
                event_status=event_no_id.event_status,
                parent_id=event_no_id.parent_id,
                local_id=new_local_id,
            )
            event_id = await self.events_repository.add_one(event)
            if event_id:
                new_event = EventSchema(
                    user_id=event.user_id,
                    name=event.name,
                    description=event.description,
                    event_status=event_no_id.event_status,
                    parent_id=event.parent_id,
                    local_id=event.local_id,
                    id=event_id,
                )
                await self.redis_repository.add_one(new_event)
                return new_event
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

    async def update_event_by_local_id(
        self,
        user: LoggedUserSchema,
        event_local_id: int,
        event_data: EventToUpdateSchema,
    ) -> bool:
        local_ids = await self.events_repository.get_local_ids(user.id)
        if event_local_id not in local_ids:
            raise not_found_error
        if (
            event_data.parent_id
            and event_data.parent_id >= event_local_id
            and event_data.parent_id not in local_ids
        ):
            raise HTTPException(
                status_code=422,
                detail="parent event not create",
            )
        update_data = event_data.model_dump(exclude_unset=True)
        if "parent_id" not in update_data:
            update_data["parent_id"] = None
        status = await self.events_repository.update_one(
            user_id=user.id,
            local_id=event_local_id,
            update_data=update_data,
        )
        if not status:
            raise unknown_error
        return status

    async def get_user_events_data(
        self,
        user: LoggedUserSchema,
    ) -> dict:
        try:
            events = await self.events_repository.get_all(user.id)
            if not events:
                events_total = None
                trees_total = None
            else:
                events_total = len(events)
                trees_total = len(
                    [event for event in events if event.parent_id == None]
                )
            return {
                "trees_total": trees_total,
                "events_total": events_total,
            }
        except Exception as e:
            logger.error(f"Unknown error: {e}")
            raise unknown_error
