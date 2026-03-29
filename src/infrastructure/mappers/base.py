from abc import abstractmethod
from typing import TypeVar, Protocol

from domain.entities import Entity
from infrastructure.database.base import Base

E = TypeVar("E", bound=Entity)
M = TypeVar("M", bound=Base)


class Mapper(Protocol[E, M]):
    @abstractmethod
    def to_domain(self, model: M) -> E: ...

    @abstractmethod
    def to_model(self, entity: E, existing: M | None) -> M: ...
