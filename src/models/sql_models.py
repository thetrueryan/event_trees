from datetime import datetime
from typing import Annotated
from enum import Enum

from sqlalchemy import (
    ForeignKey, 
    text
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped, 
    mapped_column, 
    relationship
)

# types
created_at = Annotated[
    datetime, mapped_column(
        server_default=text("TIMEZONE ('utc', now())")
        )
    ]
updated_at = Annotated[
    datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())")
        )
    ]
intpk = Annotated[int, mapped_column(primary_key=True)]
usersintfk = Annotated[int, ForeignKey("users.id")]
str_100 = Annotated[str, 100]
str_300 = Annotated[str, 300]
email_or_name_str = Annotated[
    str_100, mapped_column(nullable=False, unique=True)
    ]


class Status(Enum):
    ACTIVE = True
    INACTIVE = False


class Base(DeclarativeBase):
    pass


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[email_or_name_str]
    email: Mapped[email_or_name_str]
    password: Mapped[str_100] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    user_status: Mapped[Status] = mapped_column(default=Status.ACTIVE)

    events: Mapped[list["EventsOrm"]] = relationship(back_populates="user")

class EventsOrm(Base):
    __tablename__ = "events"

    id: Mapped[intpk]
    user_id: Mapped[usersintfk]
    local_id: Mapped[int]
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("events.id"), 
        nullable=True
        )
    description: Mapped[str_300]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    event_status: Mapped[Status] = mapped_column(default=Status.ACTIVE)

    user: Mapped["UsersOrm"] = relationship(back_populates="events")
