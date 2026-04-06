from domain.entities.artist import Artist
from presentation.api.subsonic.mappers.album import to_album_entry


def to_artist_entry(artist: Artist) -> dict:
    return {
        "@id": str(artist.id),
        "@name": artist.name,
        "@albumCount": artist.album_count,
        "@coverArt": f"ar-{artist.id}",
    }


def to_get_artist_response(artist: Artist) -> dict:
    payload = to_artist_entry(artist)
    payload["album"] = [to_album_entry(album) for album in artist.albums]
    return {
        "artist": payload
    }


def to_indexes_response(artists: list[Artist]) -> dict:
    grouped: dict[str, list[dict]] = {}
    for artist in sorted(artists, key=lambda item: item.name.lower()):
        first = artist.name[:1].upper() if artist.name else "#"
        index_name = first if first.isalpha() else "#"
        grouped.setdefault(index_name, []).append(to_artist_entry(artist))

    index_items = [
        {"@name": name, "artist": artist_items}
        for name, artist_items in grouped.items()
    ]

    return {"index": index_items}
