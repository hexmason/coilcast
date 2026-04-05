from domain.entities import Album, MediaFile
from domain.value_objects import ImageUrls, MediaFileMetadata, FileInfo
from infrastructure.database.mappers.base import Mapper
from infrastructure.database.models import AlbumModel, MediaFileModel


class AlbumMapper(Mapper):
    def to_domain(self, model: AlbumModel) -> Album:
        media_files = []
        for m in model.media_files:
            media_files.append(
                MediaFile(
                    id=m.id,
                    title=m.title,
                    track_number=m.track_number,
                    disc_number=m.disc_number,
                    created_at=m.created_at,
                    year=m.year,
                    duration=m.duration,
                    compilation=m.compilation,
                    metadata=MediaFileMetadata(
                        bit_rate=m.bit_rate,
                        bit_depth=m.bit_depth,
                        sampling_rate=m.sampling_rate,
                        channel_count=m.channel_count
                    ),
                    file_info=FileInfo(
                        path=m.path,
                        size=m.size,
                        mtime=m.mtime,
                        hash=m.hash,
                        suffix=m.suffix
                    ),
                    artist_id=model.artist_id,
                    artist_name=model.artist.name,
                    album_id=model.id,
                    album_name=model.name
                )
            )
        return Album(
            id=model.id,
            name=model.name,
            created_at=model.created_at,
            year=model.year,
            compilation=model.compilation,
            comment=model.comment,
            image_urls=ImageUrls(
                small=model.small_image_url,
                medium=model.medium_image_url,
                large=model.large_image_url
            ),
            artist_id=model.artist_id,
            artist_name=model.artist.name,
            song_count=model.song_count,
            duration=model.duration,
            play_count=model.play_count,
            media_files=media_files,
        )


    def to_model(self, entity: Album, existing: AlbumModel | None) -> AlbumModel:
        album_model = existing or AlbumModel(id=entity.id)

        album_model.name = entity.name
        album_model.created_at = entity.created_at
        album_model.year = entity.year
        album_model.compilation = entity.compilation
        album_model.comment = entity.comment
        album_model.small_image_url = entity.image_urls.small
        album_model.medium_image_url = entity.image_urls.medium
        album_model.large_image_url = entity.image_urls.large
        album_model.song_count = entity.song_count
        album_model.duration = entity.duration
        album_model.play_count = entity.play_count

        existing_media_files = {
            m.id: m for m in getattr(album_model, "media_files", [])
        }
        new_media_files = []

        for media_file in entity.media_files:
            media_file_model = existing_media_files.get(media_file.id) or MediaFileModel(
                id=media_file.id
            )
            media_file_model.album = album_model
            media_file_model.title = media_file.title
            media_file_model.track_number = media_file.track_number
            media_file_model.disc_number = media_file.disc_number
            media_file_model.created_at = media_file.created_at
            media_file_model.year = media_file.year
            media_file_model.duration = media_file.duration
            media_file_model.compilation = media_file.compilation
            media_file_model.path = media_file.file_info.path
            media_file_model.size = media_file.file_info.size
            media_file_model.mtime = media_file.file_info.mtime
            media_file_model.hash = media_file.file_info.hash
            media_file_model.suffix = media_file.file_info.suffix
            media_file_model.bit_rate = media_file.metadata.bit_rate
            media_file_model.bit_depth = media_file.metadata.bit_depth
            media_file_model.sampling_rate = media_file.metadata.sampling_rate
            media_file_model.channel_count = media_file.metadata.channel_count
            new_media_files.append(media_file_model)

        album_model.media_files[:] = new_media_files
        return album_model
