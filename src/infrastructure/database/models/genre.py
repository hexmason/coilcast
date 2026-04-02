from sqlalchemy.orm import Mapped

from infrastructure.database.models.base import Base
from infrastructure.database.types import uuid_pk, str_column


class GenreModel(Base):
    __tablename__ = "genre"

    id: Mapped[uuid_pk]
    name: Mapped[str_column]
