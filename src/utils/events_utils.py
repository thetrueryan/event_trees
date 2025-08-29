from src.schemas.event_schemas import EventSchema
from src.models.sql_models import EventsOrm


def events_from_orm_to_schema(event: EventsOrm) -> EventSchema:
    event_schema = EventSchema(
        user_id=event.user_id,
        name=event.name,
        description=event.description,
        event_status=event.event_status,
        local_id=event.local_id,
        parent_id=event.parent_id,
        id=event.id,
    )
    return event_schema
