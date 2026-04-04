from uuid import UUID
from fastapi import Depends

from infrastructure.repositories.album import AlbumRepository


class GetAlbumWithSongsUseCase():
    def __init__(self, repo: AlbumRepository = Depends()) -> None:
        self.repo = repo

    async def execute(self, id: UUID):
        return await self.repo.get_by_id_with_songs(id)
