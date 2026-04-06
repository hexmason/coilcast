from uuid import UUID


class ApplicationError(Exception):
    pass


class EntityNotFoundError(ApplicationError):
    def __init__(self, entity: str, id: UUID) -> None:
        self.entity = entity
        self.id = id
        super().__init__(f"{entity} with ID {id} not found.")
