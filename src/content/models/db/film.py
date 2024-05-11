from src.content.models.base import FilmFullMixin


class FilmDB(FilmFullMixin):
    permissions: list[dict[str, str]] | None
