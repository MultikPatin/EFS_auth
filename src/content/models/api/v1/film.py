from src.content.models.base import FilmFullMixin, FilmMixin


class Film(FilmFullMixin):
    pass


class FilmForFilmsList(FilmMixin):
    pass
