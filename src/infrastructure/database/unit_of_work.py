from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable, Awaitable


from infrastructure.repositories import (
        ArtistRepository,
        AlbumRepository,
        MediaFileRepository,
        GenreRepository,
        UserRepository
)


class UnitOfWork:
    def __init__(self, session_factory: Callable[[], Awaitable[AsyncSession]]):
        self._session_factory = session_factory
        self._session: AsyncSession

        self._artist_repo: ArtistRepository | None = None
        self._album_repo: AlbumRepository | None = None
        self._media_file_repo: MediaFileRepository | None = None
        self._genre_repo: GenreRepository | None = None
        self._user_repo: UserRepository | None = None

    async def __aenter__(self) -> "UnitOfWork":
        self._session: AsyncSession = await self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                await self._session.rollback()
            else:
                await self._session.commit()
        finally:
            await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    @property
    def artist_repo(self) -> ArtistRepository:
        if self._artist_repo is None:
            self._artist_repo = ArtistRepository(self._session)
        return self._artist_repo

    @property
    def album_repo(self) -> AlbumRepository:
        if self._album_repo is None:
            self._album_repo = AlbumRepository(self._session)
        return self._album_repo

    @property
    def media_file_repo(self) -> MediaFileRepository:
        if self._media_file_repo is None:
            self._media_file_repo = MediaFileRepository(self._session)
        return self._media_file_repo

    @property
    def genre_repo(self) -> GenreRepository:
        if self._genre_repo is None:
            self._genre_repo = GenreRepository(self._session)
        return self._genre_repo

    @property
    def user_repo(self) -> UserRepository:
        if self._user_repo is None:
            self._user_repo = UserRepository(self._session)
        return self._user_repo
