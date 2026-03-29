from domain.entities import Album, MediaFile
from domain.value_objects import MediaFileMetadata, FileInfo
from infrastructure.database.mappers import Mapper
from infrastructure.database.models import (
        MediaFileModel
)


class MediaFileMapper(Mapper):
    def to_domain(self, model: MediaFileModel) -> MediaFile:
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
            )
        )


    def to_model(self, entity: Album, existing: MediaFileModel | None) -> MediaFileModel:
        raise NotImplementedError
