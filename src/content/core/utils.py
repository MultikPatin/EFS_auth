from src.content.models.api.v1.person import FilmForPerson
from src.content.models.db.person import PersonDB


def build_films_field(person: PersonDB) -> list[FilmForPerson] | None:
    if person.films:
        return [
            FilmForPerson(uuid=film.uuid, roles=film.roles)
            for film in person.films
        ]
    else:
        return None
