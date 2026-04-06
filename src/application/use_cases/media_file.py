from uuid import UUID

from infrastructure.database.unit_of_work import UnitOfWork


class GetMediaFileUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, id: UUID):
        return await self._uow.media_file_repo.get_by_id(id)
