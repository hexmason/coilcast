from uuid import UUID
from fastapi import Depends

from infrastructure.repositories.media_file import MediaFileRepository


class GetMediaFileUseCase():
    def __init__(self, repo: MediaFileRepository = Depends()) -> None:
        self.repo = repo

    async def execute(self, id: UUID):
        return await self.repo.get_by_id(id)
