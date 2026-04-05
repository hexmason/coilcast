from sqlalchemy.orm import Mapped, relationship

from infrastructure.database.models.base import Base
from infrastructure.database.types import (
    uuid_pk,
    str_column,
    str_column_indexed,
    int_column,
)


class ArtistModel(Base):
    __tablename__ = "artist"

    id: Mapped[uuid_pk]
    name: Mapped[str_column_indexed]
    biography: Mapped[str_column]
    music_brainz_id: Mapped[str_column]
    small_image_url: Mapped[str_column]
    medium_image_url: Mapped[str_column]
    large_image_url: Mapped[str_column]
    album_count: Mapped[int_column]

    albums = relationship(
        "AlbumModel",
        back_populates="artist",
        cascade="all, delete-orphan")
