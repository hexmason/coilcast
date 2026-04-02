import datetime
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import Base
from infrastructure.database.types import (
    uuid_pk,
    created_at,
    updated_at
)


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
    is_admin: Mapped[bool]
    last_login_at: Mapped[datetime.datetime | None]
    last_access_at: Mapped[datetime.datetime | None]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
