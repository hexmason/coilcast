from uuid import uuid4, UUID
from dataclasses import dataclass

from domain.entities import Entity


@dataclass
class User(Entity):
    id: UUID
    name: str
    email: str
    hashed_password: str
    is_admin: bool = False

    @staticmethod
    def create(
        name,
        email,
        hashed_password,
        is_admin
    ) -> "User":
        return User(
            id=uuid4(),
            name=name,
            email=email,
            hashed_password=hashed_password,
            is_admin=is_admin
        )

    def change_name(self, new_name) -> None:
        if not new_name:
            raise ValueError("Name cannot be empty")
        self.name = new_name

    def change_email(self, new_email) -> None:
        if not new_email:
            raise ValueError("Email cannot be empty")
        self.email = new_email

    def change_password(self, new_hashed_password) -> None:
        self.hashed_password = new_hashed_password

    def set_admin_role(self) -> None:
        self.is_admin = True

    def unset_admin_role(self) -> None:
        self.is_admin = False
