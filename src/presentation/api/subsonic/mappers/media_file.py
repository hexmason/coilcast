from domain.entities.media_file import MediaFile
from presentation.api.subsonic.utils import get_content_type


def to_song_entry(media_file: MediaFile) -> dict:
    return {
        "@id": str(media_file.id),
        "@parent": str(media_file.album_id) if media_file.album_id else "",
        "@isDir": False,
        "@title": media_file.title,
        "@album": media_file.album_name,
        "@artist": media_file.artist_name,
        "@track": media_file.track_number,
        "@year": media_file.year,
        "@coverArt": f"mf-{media_file.id}",
        "@size": media_file.file_info.size,
        "@contentType": get_content_type(media_file.file_info.suffix),
        "@suffix": media_file.file_info.suffix.lstrip("."),
        "@duration": int(media_file.duration),
        "@bitRate": media_file.metadata.bit_rate,
        "@bitDepth": media_file.metadata.bit_depth,
        "@samplingRate": media_file.metadata.sampling_rate,
        "@channelCount": media_file.metadata.channel_count,
        "@path": media_file.file_info.path,
        "@playCount": media_file.play_count,
        "@discNumber": media_file.disc_number,
        "@created": media_file.created_at.isoformat(),
        "@albumId": str(media_file.album_id) if media_file.album_id else "",
        "@artistId": str(media_file.artist_id) if media_file.artist_id else "",
        "@type": "music",
        "@isVideo": False,
    }


def to_get_song_response(media_file: MediaFile) -> dict:
    return {"song": to_song_entry(media_file)}
