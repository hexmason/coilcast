from uuid import UUID
from fastapi import Depends

from infrastructure.repositories.artist import ArtistRepository


class GetArtistWithAlbumsUseCase():
    def __init__(self, repo: ArtistRepository = Depends()) -> None:
        self.repo = repo

    async def execute(self, id: UUID):
        return await self.repo.get_by_id_with_albums(id)


class GetArtistsUseCase():
    def __init__(self, repo: ArtistRepository = Depends()) -> None:
        self.repo = repo

    async def execute(self, id: UUID):
        return await self.repo.get_all()
