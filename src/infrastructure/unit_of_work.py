from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories import (
        ArtistRepository,
        AlbumRepository,
        MediaFileRepository,
        GenreRepository,
        UserRepository
)


class UnitOfWork:
    def __init__(self, session_factory):
        self._session_factory = session_factory
        # self.artist_repo: ArtistRepository | None = None
        # self.album_repo: AlbumRepository | None = None
        # self.media_file_repo: MediaFileRepository | None = None
        # self.genre_repo: GenreRepository | None = None
        # self.user_repo: UserRepository | None = None

    async def __aenter__(self) -> "UnitOfWork":
        self.session: AsyncSession = self._session_factory()
        self.artist_repo = ArtistRepository(self.session)
        self.album_repo = AlbumRepository(self.session)
        self.media_file_repo = MediaFileRepository(self.session)
        self.genre_repo = GenreRepository(self.session)
        self.user_repo = UserRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
            await self.session.close()
            return False
        try:
            await self.session.commit()
        finally:
            await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
