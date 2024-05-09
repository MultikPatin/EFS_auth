from django.contrib import admin

from .models import (
    FilmWork,
    Genre,
    GenreFilmWork,
    Permission,
    PermissionFilmWork,
    Person,
    PersonFilmWork,
)


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork


class PermissionFilmWorkInline(admin.TabularInline):
    model = PermissionFilmWork


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (
        GenreFilmWorkInline,
        PersonFilmWorkInline,
        PermissionFilmWorkInline,
    )
    autocomplete_fields = ("genres", "persons", "permissions")
    list_display = (
        "id",
        "title",
        "description",
        "type",
        "creation_date",
        "rating",
    )
    list_filter = (
        "type",
        "creation_date",
        "rating",
    )
    list_editable = (
        "title",
        "type",
        "description",
        "creation_date",
        "rating",
    )
    search_fields = ("title", "description", "id")
    ordering = (
        "rating",
        "title",
        "creation_date",
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_editable = ("description",)
    search_fields = ("name", "id")


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_editable = ("description",)
    search_fields = ("name", "id")


@admin.register(PermissionFilmWork)
class PermissionFilmWorkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "film_work",
        "permission",
    )
    list_editable = (
        "film_work",
        "permission",
    )
    list_filter = ("film_work",)
    search_fields = ("film_work",)
    ordering = ("film_work",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name",)
    search_fields = ("full_name", "id")
