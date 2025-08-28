from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class EmailSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr


class UserSchema(EmailSchema):
    model_config = EmailSchema.model_config

    active_status: bool = True

    @field_validator("active_status")
    def validate_status(cls, status: bool) -> bool:
        if not status:
            raise ValueError("User Inactive")
        return status


class UserAuthSchema(UserSchema):
    model_config = UserSchema.model_config

    password: str = Field(min_length=8, max_length=64)


class UserRegisterSchema(UserAuthSchema):
    model_config = UserAuthSchema.model_config

    username: str = Field(min_length=3, max_length=100)


class LoggedUserSchema(UserSchema):
    model_config = UserSchema.model_config

    username: str = Field(min_length=3, max_length=100)
    id: int = Field(ge=1)


class HashedUserSchema(UserSchema):
    model_config = UserSchema.model_config

    username: str = Field(min_length=3, max_length=100)
    password: bytes
