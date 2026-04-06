from uuid import UUID

from infrastructure.database.unit_of_work import UnitOfWork


class GetArtistWithAlbumsUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, id: UUID):
        return await self._uow.artist_repo.get_by_id_with_albums(id)


class GetArtistsUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self):
        return await self._uow.artist_repo.get_all()
