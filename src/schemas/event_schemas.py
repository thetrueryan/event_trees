from pydantic import BaseModel, Field, ConfigDict, field_validator


class NoIdsEventSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    user_id: int = Field(ge=1)
    description: str = Field(ge=3, le=300)
    event_status: bool = True
    parent_id: int = Field(ge=1)


class EventSchema(NoIdsEventSchema):
    model_config = NoIdsEventSchema.model_config

    local_id: int = Field(ge=1)

    @field_validator("parent_id")
    def validate_parent_id(cls, parent_id: int, values: dict) -> int:
        if parent_id >= values["local_id"]:
            raise ValueError("parent_id must be less than local_id")
        return parent_id
