from domain.entities.album import Album
from presentation.api.subsonic.utils import get_content_type


def to_get_album_response(album: Album):
    return {
        "album": {
            "@id": str(album.id),
            "@parent": str(album.artist_id),
            "@album": album.name,
            "@title": album.name,
            "@name": album.name,
            "@isDir": True,
            "@coverArt": "al-200000021",
            "@songCount": album.song_count,
            "@created": album.created_at,
            "@duration": album.duration,
            "@playCount": album.play_count,
            "@artistId": str(album.artist_id),
            "@artist": "Comfort Fit",
            "@year": album.year,
            "@genre": album.media_files[0].genre,  # блять
            "song": [
                {
                    "@id": str(media_file.id),
                    "@parent": str(album.id),
                    "@title": media_file.title,
                    "@isDir": False,
                    "@isVideo": False,
                    "@type": "music",
                    "@albumId": album.id,
                    "@album": album.name,
                    "@artistId": album.artist_id,
                    "@artist": album.artist_name,
                    "@coverArt": str(media_file.id),
                    "@duration": media_file.duration,
                    "@bitRate": media_file.metadata.bit_rate,
                    "@bitDepth": media_file.metadata.bit_depth,
                    "@samplingRate": media_file.metadata.sampling_rate,
                    "@channelCount": media_file.metadata.channel_count,
                    "@track": media_file.track_number,
                    "@year": media_file.year,
                    "@genre": media_file.genre,
                    "@size": media_file.file_info.size,
                    "@discNumber": media_file.discNumber,
                    "@suffix": media_file.file_info.suffix,
                    "@contentType": get_content_type(media_file.file_info.suffix),
                    "@path": media_file.file_info.path,
                }
                for media_file in album.media_files
            ],
        }
    }
