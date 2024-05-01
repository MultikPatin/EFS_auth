from src.content.models.base import UUIDMixin


class GenreDB(UUIDMixin):
    name: str
    description: str | None
