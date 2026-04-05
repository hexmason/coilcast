from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.entities import Artist
from infrastructure.database.models import AlbumModel
from infrastructure.database.models import ArtistModel
from infrastructure.database.mappers import ArtistMapper
from infrastructure.repositories.base import SQLAlchemyRepository


class ArtistRepository(SQLAlchemyRepository[Artist, ArtistModel]):
    _model = ArtistModel
    _mapper = ArtistMapper()

    async def get_by_name(self, name: str) -> Artist | None:
        stmt = select(self._model).where(self._model.name == name)
        model = await self._session.scalar(stmt)
        if not model:
            return None
        return self._mapper.to_domain(model)

    async def get_all_full(self) -> list[Artist]:
        stmt = select(ArtistModel).options(
            selectinload(ArtistModel.albums)
            .selectinload(AlbumModel.media_files)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._mapper.to_domain(model) for model in models]

    async def get_by_id_with_albums(self, id: UUID) -> Artist | None:
        stmt = (
            select(ArtistModel)
            .where(ArtistModel.id == id)
            .options(selectinload(ArtistModel.albums))
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self._mapper.to_domain(model)

    async def get_by_id_full(self, id: UUID) -> Artist | None:
        stmt = (
            select(ArtistModel)
            .where(ArtistModel.id == id)
            .options(
                selectinload(ArtistModel.albums)
                .selectinload(AlbumModel.media_files)
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self._mapper.to_domain(model)
