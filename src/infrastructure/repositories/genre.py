from domain.entities import Genre
from infrastructure.database.models import GenreModel
from infrastructure.database.mappers import GenreMapper
from infrastructure.repositories.base import SQLAlchemyRepository


class GenreRepository(SQLAlchemyRepository[Genre, GenreModel]):
    _model = GenreModel
    _mapper = GenreMapper()
