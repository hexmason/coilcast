from domain.entities import User
from infrastructure.database.mappers.base import Mapper
from infrastructure.database.models import UserModel


class UserMapper(Mapper):
    def to_domain(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            hashed_password=model.hashed_password,
            is_admin=model.is_admin,
        )

    def to_model(self, entity: User, existing: UserModel | None) -> UserModel:
        user_model = existing or UserModel(id=entity.id)
        user_model.name = entity.name
        user_model.email = entity.email
        user_model.hashed_password = entity.hashed_password
        user_model.is_admin = entity.is_admin
        return user_model
