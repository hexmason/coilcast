from domain.entities import User
from infrastructure.database.models import UserModel
from infrastructure.database.mappers import UserMapper
from infrastructure.repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User, UserModel]):
    _model = UserModel
    _mapper = UserMapper()
