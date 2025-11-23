from uuid import UUID
from domain.exceptions import AlreadyExistsError, NotFoundError


class ArtistNotFoundError(NotFoundError):
    def __init__(self, id: UUID) -> None:
        super().__init__(f"Artist with ID {id} not found.")


class ArtistExistsError(AlreadyExistsError):
    def __init__(self, id: UUID) -> None:
        super().__init__(f"Artist with ID {id} already exists.")
