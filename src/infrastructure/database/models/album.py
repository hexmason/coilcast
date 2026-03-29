from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.base import Base
from infrastructure.db.types import (
    uuid_pk,
    str_column,
    int_column,
    float_column,
    bool_column,
    created_at,
)


class AlbumModel(Base):
    __tablename__ = "album"

    id: Mapped[uuid_pk]
    name: Mapped[str_column]
    created_at: Mapped[created_at]
    year: Mapped[int_column]
    compilation: Mapped[bool_column]
    comment: Mapped[str_column]
    small_image_url: Mapped[str_column]
    medium_image_url: Mapped[str_column]
    large_image_url: Mapped[str_column]
    song_count: Mapped[int_column]
    duration: Mapped[float_column]
    play_count: Mapped[int_column]

    artist_id: Mapped[UUID] = mapped_column(
        ForeignKey("artist.id"))
    artist = relationship("ArtistModel", back_populates="albums")
    media_files = relationship(
        "MediaFileModel",
        back_populates="album",
        cascade="all, delete-orphan")
