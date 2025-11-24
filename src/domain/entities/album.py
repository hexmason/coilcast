from uuid import uuid4, UUID
from datetime import datetime
from dataclasses import dataclass, field

from domain.entities import Entity, MediaFile
from domain.value_objects import ImageUrls
from domain.exceptions import (
        MediaFileExistsError,
        MediaFileNotFoundError
)


@dataclass
class Album(Entity):
    id: UUID
    name: str
    created_at: datetime
    year: int
    compilation: bool
    comment: str
    image_urls: ImageUrls
    song_count: int = field(default=0)
    duration: float = field(default=0.0)
    play_count: int = field(default=0)
    media_files: list = field(default_factory=list)

    @staticmethod
    def create(
        name: str | None,
        compilation: bool | None,
        year: int | None,
        comment: str | None,
        image_urls: ImageUrls | None
    ) -> "Album":
        name = name or "Unknown Album"
        compilation = compilation or False
        year = year or 0
        comment = comment or ""
        image_urls = image_urls or ImageUrls()

        return Album(
            id=uuid4(),
            name=name,
            created_at=datetime.now(),
            compilation=compilation,
            year=year,
            comment=comment,
            image_urls=image_urls
        )

    def increase_play_count(self) -> None:
        self.play_count += 1

    def add_media_file(self, media_file: MediaFile) -> None:
        if any(m.id == media_file.id for m in self.media_files):
            raise MediaFileExistsError(media_file.id)

        self.media_files.append(media_file)
        self.song_count += 1
        self.duration += media_file.duration
        self.compilation = self.compilation or media_file.compilation

    def remove_media_file(self, media_file_id: UUID) -> None:
        media_file = next(
            (m for m in self.media_files if m.id == media_file_id), None)
        if not media_file:
            raise MediaFileNotFoundError(media_file_id)

        self.media_files.remove(media_file)
        self.song_count -= 1
        self.duration -= media_file.duration
        self.compilation = any(m.compilation for m in self.media_files)
