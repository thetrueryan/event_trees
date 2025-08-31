from pydantic import BaseModel, Field, ConfigDict, field_validator, ValidationInfo

from src.models.sql_models import EventStatus


class NoIdsEventSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=3, max_length=300)
    event_status: str | EventStatus
    parent_id: int | None = Field(ge=1, default=None)

    @field_validator("event_status")
    def validate_event_status(
        cls, event_status: str | EventStatus, info: ValidationInfo
    ) -> EventStatus:
        if isinstance(event_status, EventStatus):
            return event_status

        try:
            return EventStatus(event_status.lower())
        except ValueError:
            raise ValueError("event status must be past, current or future!")


class UserIdEventSchema(NoIdsEventSchema):
    model_config = NoIdsEventSchema.model_config

    user_id: int = Field(ge=1)


class LocalIdEventSchema(UserIdEventSchema):
    model_config = UserIdEventSchema.model_config

    local_id: int = Field(ge=1)


class EventSchema(LocalIdEventSchema):
    model_config = LocalIdEventSchema.model_config

    id: int = Field(ge=1)


class EventToUpdateSchema(BaseModel):

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, min_length=3, max_length=300)
    event_status: EventStatus | None = None
    parent_id: int | None = Field(None, ge=1)

    @field_validator("event_status")
    def validate_event_status(
        cls, event_status: str | EventStatus, info: ValidationInfo
    ) -> EventStatus:
        if isinstance(event_status, EventStatus):
            return event_status

        try:
            return EventStatus(event_status.lower())
        except ValueError:
            raise ValueError("event status must be past, current or future!")
