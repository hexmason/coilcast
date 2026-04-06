from uuid import UUID
from abc import abstractmethod
from typing import Protocol, TypeVar

from domain.entities.base import Entity

E = TypeVar("E", bound=Entity)


class Repository(Protocol[E]):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> E | None: ...

    @abstractmethod
    async def get_all(self) -> list[E]: ...

    @abstractmethod
    async def save(self, entity: E) -> None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...
