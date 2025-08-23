from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class EmailSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr


class UserSchema(EmailSchema):
    model_config = EmailSchema.model_config

    username: str = Field(min_length=3, max_length=100)
    active_status: bool = True

    @field_validator("active_status")
    def validate_status(cls, status: bool) -> bool:
        if not status:
            raise ValueError("User Inactive")
        return status


class UserAuthSchema(UserSchema):
    model_config = UserSchema.model_config

    password: str = Field(min_length=8, max_length=64)


class LoggedUserSchema(UserSchema):
    model_config = UserSchema.model_config

    id: int = Field(ge=1)


class HashedUserSchema(UserSchema):
    model_config = UserSchema.model_config

    password: bytes
