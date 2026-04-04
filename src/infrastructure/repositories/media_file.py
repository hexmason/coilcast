from sqlalchemy import select

from domain.entities import MediaFile
from infrastructure.database.models import MediaFileModel
from infrastructure.database.mappers import MediaFileMapper
from infrastructure.repositories.base import SQLAlchemyRepository


class MediaFileRepository(SQLAlchemyRepository[MediaFile, MediaFileModel]):
    _model = MediaFileModel
    _mapper = MediaFileMapper()

    async def get_by_path(self, path: str) -> MediaFile | None:
        stmt = select(self._model).where(self._model.path == path)
        model = await self._session.scalar(stmt)
        if not model:
            return None
        return self._mapper.to_domain(model)
