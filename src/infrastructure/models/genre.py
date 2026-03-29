from sqlalchemy.orm import Mapped

from infrastructure.db.base import Base
from infrastructure.db.types import uuid_pk, str_column


class GenreModel(Base):
    __tablename__ = "genre"

    id: Mapped[uuid_pk]
    name: Mapped[str_column]
