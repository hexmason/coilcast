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

    async def get_by_id_with_songs(self, id: UUID) -> list[Album]:
        stmt = (
            select(AlbumModel)
            .where(AlbumModel.id == id)
            .options(
                selectinload(AlbumModel.media_files)
            )
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._mapper.to_domain(model) for model in models]
