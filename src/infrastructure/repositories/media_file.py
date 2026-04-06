from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.entities import MediaFile
from infrastructure.database.models.album import AlbumModel
from infrastructure.database.models import MediaFileModel
from infrastructure.database.mappers import MediaFileMapper
from infrastructure.repositories.base import SQLAlchemyRepository


class MediaFileRepository(SQLAlchemyRepository[MediaFile, MediaFileModel]):
    _model = MediaFileModel
    _mapper = MediaFileMapper()

    async def get_by_id(self, id: UUID) -> MediaFile | None:
        stmt = (
            select(self._model)
            .where(self._model.id == id)
            .options(selectinload(MediaFileModel.album).selectinload(AlbumModel.artist))
        )
        model = await self._session.scalar(stmt)
        if not model:
            return None
        return self._mapper.to_domain(model)

    async def get_by_path(self, path: str) -> MediaFile | None:
        stmt = (
            select(self._model)
            .where(self._model.path == path)
            .options(selectinload(MediaFileModel.album).selectinload(AlbumModel.artist))
        )
        model = await self._session.scalar(stmt)
        if not model:
            return None
        return self._mapper.to_domain(model)
