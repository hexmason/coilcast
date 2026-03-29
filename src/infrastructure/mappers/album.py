from domain.entities import Album, MediaFile
from domain.value_objects import ImageUrls, MediaFileMetadata, FileInfo
from infrastructure.database.mappers import Mapper
from infrastructure.database.models import AlbumModel


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
                    )
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
            song_count=model.song_count,
            duration=model.duration,
            play_count=model.play_count
        )


    def to_model(self, entity: Album, existing: AlbumModel | None) -> AlbumModel:
        raise NotImplementedError
