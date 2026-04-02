from domain.entities import Genre
from infrastructure.database.mappers.base import Mapper
from infrastructure.database.models import GenreModel


class GenreMapper(Mapper):
    def to_domain(self, model: GenreModel) -> Genre:
        return Genre(id=model.id, name=model.name)

    def to_model(self, entity: Genre, existing: GenreModel | None) -> GenreModel:
        genre_model = existing or GenreModel(id=entity.id)
        genre_model.name = entity.name
        return genre_model
