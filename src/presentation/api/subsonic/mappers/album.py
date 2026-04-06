from domain.entities.album import Album
from presentation.api.subsonic.mappers.media_file import to_song_entry


def to_album_entry(album: Album) -> dict:
    return {
        "@id": str(album.id),
        "@parent": str(album.artist_id) if album.artist_id else "",
        "@album": album.name,
        "@title": album.name,
        "@name": album.name,
        "@isDir": True,
        "@coverArt": f"al-{album.id}",
        "@songCount": album.song_count,
        "@created": album.created_at.isoformat(),
        "@duration": int(album.duration),
        "@playCount": album.play_count,
        "@artistId": str(album.artist_id) if album.artist_id else "",
        "@artist": album.artist_name,
        "@year": album.year,
    }


def to_get_album_response(album: Album) -> dict:
    payload = to_album_entry(album)
    payload["song"] = [to_song_entry(media_file) for media_file in album.media_files]
    return {"album": payload}
