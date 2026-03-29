from uuid import UUID
from abc import abstractmethod
from typing import AsyncIterator, Protocol, TypeVar

from domain.entities.base import Entity

E = TypeVar("E", bound=Entity)


class Repository(Protocol[E]):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> E | None: ...

    @abstractmethod
    def get_all(self) -> AsyncIterator[Entity]: ...

    @abstractmethod
    async def save(self, entity: E) -> None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...
