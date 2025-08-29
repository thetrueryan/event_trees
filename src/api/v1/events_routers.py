from fastapi import APIRouter, Depends

from src.schemas.user_schemas import LoggedUserSchema
from src.schemas.event_schemas import NoIdsEventSchema, LocalIdEventSchema
from src.services.events_service import EventsService
from src.utils.dependencies import get_current_auth_user, get_events_service


router = APIRouter(tags=["Пользователь", "События"])


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
    user: LoggedUserSchema = Depends(get_current_auth_user),  # validate, dont delete!
    service: EventsService = Depends(get_events_service),
):
    event = await service.add_event(user=user, event_no_id=event_no_id)
    return event
