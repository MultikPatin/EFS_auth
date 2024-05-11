from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request

from src.content.models.api.v1.film import Film, FilmForFilmsList
from src.content.services.current_user import (
    CurrentUserService,
    JWTBearer,
    get_current_user,
    security_jwt,
)
from src.content.services.film import FilmService, get_film_service
from src.content.validators.films import FilmFieldsToSort
from src.content.validators.pagination import (
    PaginatedParams,
    get_paginated_params,
)
from src.content.validators.search import search_query_validators

router = APIRouter()


@router.get("/{film_id}", response_model=Film, summary="Get film details by id")
async def film_details(
    request: Request,
    film_uuid: Annotated[
        UUID,
        Path(
            alias="film_id",
            title="film id",
            description="The UUID of the film to get",
            example="8f128d84-dd99-4d0d-a9c8-df11f87ac133",
        ),
    ],
    film_service: FilmService = Depends(get_film_service),
    role_uuid: JWTBearer = Depends(security_jwt),
    current_user: CurrentUserService = Depends(get_current_user),
) -> Film:
    """
    Get film details by id

    Args:
    - **film_id** (str): The UUID of the film to get

    Returns:
    - **Film**: The film with the given ID

    Raises:
        HTTPException: If the film does not exist
    """
    permissions = await current_user.get_permissions(role_uuid, request)
    film = await film_service.get_by_id(film_uuid, permissions)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="film not found"
        )
    return Film(
        uuid=film.uuid,
        title=film.title,
        imdb_rating=film.imdb_rating,
        genre=film.genre,
        description=film.description,
        directors=film.directors,
        actors=film.actors,
        writers=film.writers,
    )


@router.get(
    "/", response_model=list[FilmForFilmsList], summary="Get a list of films"
)
async def films(
    request: Request,
    page_number: int = 1,
    page_size: int = 50,
    genre_uuid: Annotated[
        UUID | None,
        Query(
            alias="genre",
            title="Genre UUID",
            description="The UUID of the genre to filter movies",
            example="6a0a479b-cfec-41ac-b520-41b2b007b611",
        ),
    ] = None,
    sort: Annotated[
        FilmFieldsToSort,
        Query(
            alias="sort",
            title="Sort field",
            description="The name of the field to sort movies",
            examples=["-imdb_rating", "imdb_rating", "-title.raw", "title.raw"],
        ),
    ] = FilmFieldsToSort.desc_rating,
    paginated_params: PaginatedParams = Depends(get_paginated_params),
    film_service: FilmService = Depends(get_film_service),
    role_uuid: JWTBearer = Depends(security_jwt),
    current_user: CurrentUserService = Depends(get_current_user),
) -> list[FilmForFilmsList]:
    """
    Get a list of films.

    Args:
    - **page_number** (int): The number of the page to get (default: 1)
    - **page_size** (int): The size of the page to get (default: 5)
    - **genre** (str): The UUID of the genre to filter movies
    - **sort** (ValidFieldsToSort): The name of the field to sort movies

    Returns:
    - **list[FilmForFilmsList]**: The list of films

    Raises:
        HTTPException: If no films are found
    """
    permissions = await current_user.get_permissions(role_uuid, request)
    paginated_params.validate(page_number, page_size)
    films = await film_service.get_films(
        **paginated_params.get(),
        genre_uuid=genre_uuid,
        sort=sort,
        user_permissions=permissions,
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="films not found"
        )
    return [
        FilmForFilmsList(
            uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating
        )
        for film in films
    ]


@router.get(
    "/search/",
    response_model=list[FilmForFilmsList],
    summary="Get a list of films based on a search query",
)
async def films_search_by_title(
    request: Request,
    page_number: int = 1,
    page_size: int = 50,
    search_query: Annotated[
        str | None,
        search_query_validators,
    ] = "",
    paginated_params: PaginatedParams = Depends(get_paginated_params),
    film_service: FilmService = Depends(get_film_service),
    role_uuid: JWTBearer = Depends(security_jwt),
    current_user: CurrentUserService = Depends(get_current_user),
) -> list[FilmForFilmsList]:
    """
    Get a list of films based on a search query.

    Args:
    - **page_number** (int): The number of the page to get (default: 1)
    - **page_size** (int): The size of the page to get (default: 5)
    - **query** (str): The query to search movies

    Returns:
    - **list[FilmForFilmsList]**: The list of films

    Raises:
        HTTPException: If no films are found
    """
    permissions = await current_user.get_permissions(role_uuid, request)
    field = "title"
    paginated_params.validate(page_number, page_size)
    films = await film_service.get_search(
        **paginated_params.get(),
        search_query=search_query,
        field=field,
        user_permissions=permissions,
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="films not found"
        )
    return [
        FilmForFilmsList(
            uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating
        )
        for film in films
    ]
