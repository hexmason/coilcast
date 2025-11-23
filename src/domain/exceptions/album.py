from uuid import UUID
from domain.exceptions import AlreadyExistsError, NotFoundError


class AlbumNotFoundError(NotFoundError):
    def __init__(self, id: UUID) -> None:
        super().__init__(f"Album with ID {id} not found.")


class AlbumExistsError(AlreadyExistsError):
    def __init__(self, id: UUID) -> None:
        super().__init__(f"Album with ID {id} already exists.")
