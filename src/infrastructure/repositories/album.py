from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.entities import Album
from infrastructure.database.models import AlbumModel
from infrastructure.database.mappers import AlbumMapper
from infrastructure.repositories.base import SQLAlchemyRepository


class AlbumRepository(SQLAlchemyRepository[Album, AlbumModel]):
    _model = AlbumModel
    _mapper = AlbumMapper()

    async def get_by_name(self, name: str) -> Album | None:
        stmt = select(self._model).where(self._model.name == name)
        model = await self._session.scalar(stmt)
        if not model:
            return None
        return self._mapper.to_domain(model)

    async def get_by_id_with_songs(self, id: UUID) -> Album | None:
        stmt = (
            select(AlbumModel)
            .where(AlbumModel.id == id)
            .options(
                selectinload(AlbumModel.artist),
                selectinload(AlbumModel.media_files)
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self._mapper.to_domain(model)
