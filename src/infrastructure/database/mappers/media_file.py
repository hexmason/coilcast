from domain.entities import MediaFile
from domain.value_objects import MediaFileMetadata, FileInfo
from infrastructure.database.mappers.base import Mapper
from infrastructure.database.models import MediaFileModel


class MediaFileMapper(Mapper):
    def to_domain(self, model: MediaFileModel) -> MediaFile:
        album = model.album
        artist = album.artist if album else None

        return MediaFile(
            id=model.id,
            title=model.title,
            track_number=model.track_number,
            disc_number=model.disc_number,
            created_at=model.created_at,
            year=model.year,
            duration=model.duration,
            compilation=model.compilation,
            metadata=MediaFileMetadata(
                bit_rate=model.bit_rate,
                bit_depth=model.bit_depth,
                sampling_rate=model.sampling_rate,
                channel_count=model.channel_count
            ),
            file_info=FileInfo(
                path=model.path,
                size=model.size,
                mtime=model.mtime,
                hash=model.hash,
                suffix=model.suffix
            ),
            artist_id=model.artist_id,
            artist_name=artist.name if artist else "",
            album_id=model.album_id,
            album_name=album.name if album else "",
        )


    def to_model(self, entity: MediaFile, existing: MediaFileModel | None) -> MediaFileModel:
        media_file_model = existing or MediaFileModel(id=entity.id)
        media_file_model.title = entity.title
        media_file_model.track_number = entity.track_number
        media_file_model.disc_number = entity.disc_number
        media_file_model.created_at = entity.created_at
        media_file_model.year = entity.year
        media_file_model.duration = entity.duration
        media_file_model.compilation = entity.compilation
        media_file_model.path = entity.file_info.path
        media_file_model.size = entity.file_info.size
        media_file_model.mtime = entity.file_info.mtime
        media_file_model.hash = entity.file_info.hash
        media_file_model.suffix = entity.file_info.suffix
        media_file_model.bit_rate = entity.metadata.bit_rate
        media_file_model.bit_depth = entity.metadata.bit_depth
        media_file_model.sampling_rate = entity.metadata.sampling_rate
        media_file_model.channel_count = entity.metadata.channel_count
        return media_file_model
