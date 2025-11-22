from uuid import uuid4, UUID
from dataclasses import dataclass, field

from domain.entities.base import Entity
from domain.entities.album import Album
from domain.value_objects.image_urls import ImageUrls


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
        name: str,
        album_count: int,
        biography: str,
        music_brainz_id: str,
        image_urls: ImageUrls
    ) -> "Artist":
        return Artist(
            id=uuid4(),
            name=name,
            album_count=album_count,
            biography=biography,
            music_brainz_id=music_brainz_id,
            image_urls=image_urls
        )

    def add_album(self, album: Album) -> None:
        if any(a.id == album.id for a in self.albums):
            raise ValueError("Artist already has this album")

        self.albums.append(album)
        self.album_count += 1

    def remove_album(self, album_id: UUID) -> None:
        album = next((a for a in self.albums if a.id == album_id), None)
        if not album:
            raise ValueError("Album not found for the artist")
