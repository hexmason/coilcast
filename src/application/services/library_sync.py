from application.interfaces import MetadataProvider
from application.normalizers import MetadataNormalizer
from application.services.library_scanner import LibraryScannerService
from domain.entities import Album, Artist, MediaFile
from domain.value_objects import FileInfo, MediaFileMetadata
from infrastructure.database import UnitOfWork
from infrastructure.providers.dto import FileInfoDTO
from infrastructure.providers.mappers import track_metadata_to_dto


class LibrarySyncService:
    def __init__(
        self,
        scanner: LibraryScannerService,
        metadata_provider: MetadataProvider,
        uow: UnitOfWork
    ) -> None:
        self.scanner = scanner
        self.metadata_provider = metadata_provider
        self.uow = uow

    async def sync(self) -> set[str]:
        seen_paths = set()
        artists_to_delete: set = set()

        async with self.uow:
            artists = await self.uow.artist_repo.get_all_full()

            artists_by_name = {artist.name: artist for artist in artists}
            albums_by_key = {
                (artist.id, album.name): album
                for artist in artists
                for album in artist.albums
            }
            tracks_by_path = {
                media.file_info.path: (artist, album, media)
                for artist in artists
                for album in artist.albums
                for media in album.media_files
            }

            async for file in self.scanner.scan():
                path = str(file.path)
                seen_paths.add(path)
                existing = tracks_by_path.get(path)

                if existing and self._is_unchanged(existing[2].file_info, file):
                    continue
                if existing and existing[2].file_info.hash == file.hash:
                    existing[2].update_file_info(file)
                    continue

                dto = self._get_track_metadata(file)
                artist_name = dto.artist or "Unknown artist"
                album_name = dto.album or "Unknown album"

                target_artist = artists_by_name.get(artist_name)
                if not target_artist:
                    target_artist = Artist.create(
                        name=artist_name,
                        biography=None,
                        music_brainz_id=None,
                        image_urls=None,
                    )
                    artists.append(target_artist)
                    artists_by_name[target_artist.name] = target_artist

                target_album = albums_by_key.get((target_artist.id, album_name))
                if not target_album:
                    target_album = Album.create(
                        name=album_name,
                        compilation=dto.compilation,
                        year=dto.year,
                        comment=None,
                        image_urls=None,
                        artist_id=target_artist.id,
                        artist_name=target_artist.name,
                    )
                    target_artist.add_album(target_album)
                    albums_by_key[(target_artist.id, target_album.name)] = target_album

                if existing:
                    source_artist, source_album, media = existing
                    source_album.remove_media_file(media.id)
                    if not source_album.media_files:
                        source_artist.remove_album(source_album.id)
                        albums_by_key.pop((source_artist.id, source_album.name), None)
                    if not source_artist.albums:
                        artists_to_delete.add(source_artist.id)
                    self._apply_media_updates(media, dto, file)
                else:
                    media = MediaFile.create(
                        title=dto.title,
                        track_number=dto.track_number,
                        disc_number=dto.disc_number,
                        year=dto.year,
                        duration=dto.duration,
                        compilation=dto.compilation,
                        file_info=FileInfo(
                            path=str(file.path),
                            size=file.size,
                            mtime=file.mtime,
                            hash=file.hash,
                            suffix=file.suffix
                        ),
                        artist_id=target_artist.id,
                        artist_name=target_artist.name,
                        album_id=target_album.id,
                        album_name=target_album.name,
                        metadata=MediaFileMetadata(
                            bit_rate=dto.bit_rate or 0,
                            bit_depth=dto.bit_depth or 0,
                            sampling_rate=dto.sampling_rate or 0,
                            channel_count=dto.channel_count or 0,
                        ),
                    )

                target_album.add_media_file(media)
                tracks_by_path[path] = (target_artist, target_album, media)
                artists_to_delete.discard(target_artist.id)

            db_paths = set(tracks_by_path.keys())
            for removed_path in db_paths.difference(seen_paths):
                source_artist, source_album, media = tracks_by_path.pop(removed_path)
                source_album.remove_media_file(media.id)
                if not source_album.media_files:
                    source_artist.remove_album(source_album.id)
                    albums_by_key.pop((source_artist.id, source_album.name), None)
                if not source_artist.albums:
                    artists_to_delete.add(source_artist.id)

            for artist in artists:
                if artist.id in artists_to_delete:
                    continue
                await self.uow.artist_repo.save(artist)

            for artist_id in artists_to_delete:
                await self.uow.artist_repo.delete(artist_id)

        return seen_paths

    @staticmethod
    def _is_unchanged(existing: FileInfo, scanned: FileInfoDTO) -> bool:
        return existing.size == scanned.size and existing.mtime == scanned.mtime

    def _get_track_metadata(self, file_info: FileInfoDTO):
        raw_metadata = self.metadata_provider.get_track_metadata(file_info.path)
        normalized = MetadataNormalizer.normalize(raw_metadata)
        return track_metadata_to_dto(normalized)

    @staticmethod
    def _apply_media_updates(media: MediaFile, dto, file_info: FileInfoDTO) -> None:
        if dto.title is not None:
            media.title = dto.title
        if dto.track_number is not None:
            media.track_number = dto.track_number
        if dto.disc_number is not None:
            media.disc_number = dto.disc_number
        if dto.year is not None:
            media.year = dto.year
        if dto.duration is not None:
            media.duration = dto.duration
        media.compilation = dto.compilation if dto.compilation is not None else media.compilation
        media.update_file_info(file_info)
        media.update_metadata(
            MediaFileMetadata(
                bit_rate=dto.bit_rate or 0,
                bit_depth=dto.bit_depth or 0,
                sampling_rate=dto.sampling_rate or 0,
                channel_count=dto.channel_count or 0,
            )
        )
