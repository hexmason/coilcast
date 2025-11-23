from uuid import UUID
from domain.exceptions import AlreadyExistsError, NotFoundError


class MediaFileNotFoundError(NotFoundError):
    def __init__(self, id: UUID) -> None:
        super().__init__(f"Media file with ID {id} not found.")


class MediaFileExistsError(AlreadyExistsError):
    def __init__(self, id: UUID) -> None:
        super().__init__(f"Media file with ID {id} already exists.")
