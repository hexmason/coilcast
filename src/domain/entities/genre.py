from uuid import uuid4, UUID
from dataclasses import dataclass

from domain.entities import Entity


@dataclass(frozen=True)
class Genre(Entity):
    id: UUID
    name: str

    @staticmethod
    def create(
        name: str,
    ) -> "Genre":
        return Genre(
            id=uuid4(),
            name=name
        )
