from typing import List
from domain.entities.artist import Artist


def to_get_artist_response(artist: Artist) -> dict:
    return {
        "artist": {
            "@id": str(artist.id),
            "@name": artist.name,
            "@coverArt": "",
            "@albumCount": artist.album_count,
            "@userRating": 5,
            "@artistImageUrl": artist.image_urls.large,
            "album": [
                {
                    "@id": str(album.id),
                    "@parent": str(artist.id),
                    "@album": album.title,
                    "@title": album.title,
                    "@name": album.title,
                    "@isDir": "true",
                    "@coverArt": f"al-{album.id}",
                    "@songCount": album.song_count,
                    "@created": album.created_at,
                    "@duration": album.duration,
                    "@playCount": album.play_count,
                    "@artistId": str(artist.id),
                    "@artist": artist.name,
                    "@year": album.year,
                    "@genre": album.genre,
                    "@userRating": 5,
                    "@averageRating": album.average_rating,
                    "@starred": "2017-04-11T10:42:50.842Z",
                }
                for album in artist.albums
            ],
        }
    }


def map_artists(artists: List[Artist]):
    pass
