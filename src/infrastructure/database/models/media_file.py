from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import Base
from infrastructure.database.types import (
    uuid_pk,
    str_column,
    int_column,
    float_column,
    bool_column,
    created_at,
    updated_at
)


class MediaFileModel(Base):
    __tablename__ = "media_file"

    id: Mapped[uuid_pk]
    title: Mapped[str_column]
    track_number: Mapped[int_column]
    disc_number: Mapped[int_column]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    year: Mapped[int_column]
    duration: Mapped[float_column]
    compilation: Mapped[bool_column]
    path: Mapped[str_column]
    size: Mapped[int_column]
    mtime: Mapped[float_column]
    hash: Mapped[str_column]
    suffix: Mapped[str_column]
    # offset: Mapped[float_column]
    # subtrack: Mapped[int_column]
    bit_rate: Mapped[int_column]
    bit_depth: Mapped[int_column]
    sampling_rate: Mapped[int_column]
    channel_count: Mapped[int_column]

    artist_id: Mapped[UUID] = mapped_column(
        ForeignKey("artist.id"))
    album_id: Mapped[UUID] = mapped_column(
        ForeignKey("album.id"))
    album = relationship("AlbumModel", back_populates="media_files")
