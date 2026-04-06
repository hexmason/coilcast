from uuid import UUID

from infrastructure.database.unit_of_work import UnitOfWork


class GetAlbumWithSongsUseCase():
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, id: UUID):
        return await self._uow.album_repo.get_by_id_with_songs(id)
