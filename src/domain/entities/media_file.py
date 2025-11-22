from uuid import uuid4, UUID
from datetime import datetime
from dataclasses import dataclass, field

from domain.entities.base import Entity
from domain.value_objects.media_file_metadata import MediaFileMetadata


@dataclass
class MediaFile(Entity):
    id: UUID
    title: str
    track_number: int
    disk_number: int
    created_at: datetime
    year: int
    duration: float
    compilation: bool
    metadata: MediaFileMetadata
    play_count: int = field(default=0)

    @staticmethod
    def create(
        title: str,
        track_number: int,
        disk_number: int,
        year: int,
        duration: float,
        compilation: bool,
        metadata: MediaFileMetadata
    ) -> "MediaFile":
        return MediaFile(
            id=uuid4(),
            title=title,
            track_number=track_number,
            disk_number=disk_number,
            created_at=datetime.now(),
            year=year,
            duration=duration,
            compilation=compilation,
            metadata=metadata
        )

    def update_metadata(self, metadata) -> None:
        self.metadata = metadata

    def increment_play_count(self) -> None:
        self.play_count += 1
