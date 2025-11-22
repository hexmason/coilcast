from uuid import UUID
from typing import Protocol


class Entity(Protocol):
    id: UUID
