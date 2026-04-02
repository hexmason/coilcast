from uuid import uuid4, UUID
from dataclasses import dataclass, field

from domain.entities import Entity, Album
from domain.value_objects import ImageUrls
from domain.exceptions import (
        AlbumExistsError,
        AlbumNotFoundError
)


@dataclass
class Artist(Entity):
    id: UUID
    name: str
    biography: str
    music_brainz_id: str
    image_urls: ImageUrls
    album_count: int = field(default=0)
    albums: list = field(default_factory=list)

    @staticmethod
    def create(
        name: str | None,
        biography: str | None,
        music_brainz_id: str | None,
        image_urls: ImageUrls | None
    ) -> "Artist":
        name = name or "Unknown artist"
        biography = biography or ""
        music_brainz_id = music_brainz_id or ""
        image_urls = image_urls or ImageUrls()

        return Artist(
            id=uuid4(),
            name=name,
            biography=biography,
            music_brainz_id=music_brainz_id,
            image_urls=image_urls
        )

    def add_album(self, album: Album) -> None:
        if any(a.id == album.id for a in self.albums):
            raise AlbumExistsError(album.id)

        self.albums.append(album)
        self.album_count += 1

    def remove_album(self, album_id: UUID) -> None:
        album = next((a for a in self.albums if a.id == album_id), None)
        if not album:
            raise AlbumNotFoundError(album_id)

        self.albums.remove(album)
        self.album_count -= 1
