from uuid import UUID
from typing import AsyncIterator, Generic, TypeVar, Type
from sqlalchemy import select

from domain.entities.base import Entity
from domain.interfaces import Repository
from application.exceptions import EntityNotFoundError
from infrastructure.database.models import Base
from infrastructure.database.mappers.base import Mapper

E = TypeVar("E", bound=Entity)
M = TypeVar("M", bound=Base)


class SQLAlchemyRepository(Repository[E], Generic[E, M]):
    _model: Type[M]
    _mapper: Mapper[E, M]

    def __init__(self, session) -> None:
        self._session = session

    async def get_by_id(self, id: UUID) -> E | None:
        model = await self._session.get(self._model, id)
        if not model:
            return None
        return self._mapper.to_domain(model)

    async def get_all(self) -> list[E]:
        stmt = select(self._model)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._mapper.to_domain(model) for model in models]

    async def save(self, entity: E) -> None:
        existing = await self._session.get(self._model, entity.id)
        model = self._mapper.to_model(entity, existing)
        self._session.add(model)
        await self._session.flush()

    async def delete(self, id: UUID) -> None:
        model = await self._session.get(self._model, id)
        if not model:
            raise EntityNotFoundError(self._model.__name__, id)
        await self._session.delete(model)
        await self._session.flush()
