from domain.entities import Artist, Album, MediaFile
from domain.value_objects import ImageUrls, MediaFileMetadata, FileInfo
from infrastructure.database.mappers.base import Mapper
from infrastructure.database.models import (
        ArtistModel,
        AlbumModel,
        MediaFileModel
)


class ArtistMapper(Mapper):
    def to_domain(self, model: ArtistModel) -> Artist:
        albums = []
        for a in model.albums:
            media_files = []
            for m in a.media_files:
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
                        artist_id=model.id,
                        artist_name=model.name,
                        album_id=a.id,
                        album_name=a.name
                    )
                )
            albums.append(
                Album(
                    id=a.id,
                    name=a.name,
                    created_at=a.created_at,
                    year=a.year,
                    compilation=a.compilation,
                    comment=a.comment,
                    image_urls=ImageUrls(
                        small=a.small_image_url,
                        medium=a.medium_image_url,
                        large=a.large_image_url
                    ),
                    artist_id=a.artist_id,
                    artist_name=a.artist_name,
                    song_count=a.song_count,
                    duration=a.duration,
                    play_count=a.play_count,
                    media_files=media_files,
                )
            )

        return Artist(
            id=model.id,
            name=model.name,
            biography=model.biography,
            music_brainz_id=model.music_brainz_id,
            image_urls=ImageUrls(
                small=model.small_image_url,
                medium=model.medium_image_url,
                large=model.large_image_url
            ),
            album_count=model.album_count,
            albums=albums
        )

    def to_model(self, entity: Artist, existing: ArtistModel | None) -> ArtistModel:
        artist_model = existing or ArtistModel(id=entity.id)

        artist_model.name = entity.name
        artist_model.biography = entity.biography
        artist_model.music_brainz_id = entity.music_brainz_id
        artist_model.small_image_url = entity.image_urls.small
        artist_model.medium_image_url = entity.image_urls.medium
        artist_model.large_image_url = entity.image_urls.large
        artist_model.album_count = entity.album_count

        existing_albums = {
            a.id: a for a in getattr(artist_model, "albums", [])}
        new_albums = []

        for a in entity.albums:
            album_model = existing_albums.get(a.id) or AlbumModel(id=a.id)
            album_model.artist = artist_model

            album_model.name = a.name
            album_model.created_at = a.created_at
            album_model.year = a.year
            album_model.compilation = a.compilation
            album_model.comment = a.comment
            album_model.small_image_url = a.image_urls.small
            album_model.medium_image_url = a.image_urls.medium
            album_model.large_image_url = a.image_urls.large
            album_model.song_count = a.song_count
            album_model.duration = a.duration
            album_model.play_count = a.play_count
            album_model.artist = artist_model

            existing_media_files = {
                t.id: t for t in getattr(album_model, "media_files", [])}
            new_media_files = []

            for m in a.media_files:
                media_file_model = (
                        existing_media_files.get(m.id) or
                        MediaFileModel(id=m.id)
                )
                media_file_model.album = album_model

                media_file_model.title = m.title
                media_file_model.track_number = m.track_number
                media_file_model.disc_number = m.disc_number
                media_file_model.created_at = m.created_at
                media_file_model.year = m.year
                media_file_model.duration = m.duration
                media_file_model.compilation = m.compilation
                media_file_model.path = m.file_info.path
                media_file_model.size = m.file_info.size
                media_file_model.mtime = m.file_info.mtime
                media_file_model.hash = m.file_info.hash
                media_file_model.suffix = m.file_info.suffix
                media_file_model.bit_rate = m.metadata.bit_rate
                media_file_model.bit_depth = m.metadata.bit_depth
                media_file_model.sampling_rate = m.metadata.sampling_rate
                media_file_model.channel_count = m.metadata.channel_count
                media_file_model.artist_id = m.artist_id

                new_media_files.append(media_file_model)

            album_model.media_files[:] = new_media_files
            new_albums.append(album_model)

        artist_model.albums[:] = new_albums

        return artist_model
