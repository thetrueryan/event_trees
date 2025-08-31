from src.models.sql_models import UsersOrm
from src.utils.events_utils import events_from_orm_to_schema
from src.schemas.user_schemas import ToPublicUserSchema


def from_user_orm_to_public_user(user: UsersOrm) -> ToPublicUserSchema:
    events = [events_from_orm_to_schema(event) for event in user.events]
    return ToPublicUserSchema(
        id=user.id,
        username=user.username,
        events_total=len(events),
        trees_total=len([event for event in events if event.parent_id == None]),
    )
