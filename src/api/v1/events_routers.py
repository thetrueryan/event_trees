from fastapi import APIRouter, Depends

from src.schemas.user_schemas import LoggedUserSchema
from src.schemas.event_schemas import NoIdsEventSchema, EventToUpdateSchema
from src.services.events_service import EventsService
from src.utils.dependencies import (
    get_current_auth_user,
    get_events_service,
    http_bearer,
)


router = APIRouter(
    tags=["Пользователь", "События"], dependencies=[Depends(http_bearer)]
)


@router.get("/user/events")
async def get_user_events(
    user: LoggedUserSchema = Depends(get_current_auth_user),
    service: EventsService = Depends(get_events_service),
):
    events = await service.get_events(user)
    return {"user": user, "events": events}


@router.post("/user/events/add")
async def add_user_event(
    event_no_id: NoIdsEventSchema,
    user: LoggedUserSchema = Depends(get_current_auth_user),
    service: EventsService = Depends(get_events_service),
):
    event = await service.add_event(user=user, event_no_id=event_no_id)
    return event


@router.get("/user/events/{local_id}")
async def get_user_event_by_local_id(
    local_id: int,
    user: LoggedUserSchema = Depends(get_current_auth_user),
    service: EventsService = Depends(get_events_service),
):
    event = await service.get_event_by_id(user, local_id)
    return event


@router.delete("/user/events/{local_id}")
async def delete_user_event(
    local_id: int,
    user: LoggedUserSchema = Depends(get_current_auth_user),
    service: EventsService = Depends(get_events_service),
):
    status = await service.delete_event_by_local_id(user, local_id)
    return {"status": status}


@router.patch("/user/events/{local_id}")
async def put_user_event(
    local_id: int,
    event_to_update: EventToUpdateSchema,
    user: LoggedUserSchema = Depends(get_current_auth_user),
    service: EventsService = Depends(get_events_service),
):
    status = await service.update_event_by_local_id(
        user=user, event_local_id=local_id, event_data=event_to_update
    )
    return {"status": status}
