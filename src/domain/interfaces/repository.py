from uuid import UUID
from abc import abstractmethod
from typing import AsyncIterator, TypeVar, Protocol

from domain.entities.base import Entity

E = TypeVar("E", bound=Entity)
M = TypeVar("M", covariant=True)


class Repository(Protocol[E, M]):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> E | None: ...

    @abstractmethod
    def get_all(self) -> AsyncIterator[E]: ...

    @abstractmethod
    async def save(self, entity: E) -> None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...
