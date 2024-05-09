import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class DescriptionMixin(models.Model):
    description = models.TextField(_("description"), blank=True)

    class Meta:
        abstract = True


class CreatedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TimeStampedMixin(CreatedMixin):
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class FilmWork(TimeStampedMixin, UUIDMixin, DescriptionMixin):
    class ContentType(models.TextChoices):
        MOVIE = "movie", _("movie")
        TV_SHOW = "tv_show", _("tv_show")

    title = models.CharField(_("title"), max_length=255)
    creation_date = models.DateField(_("creation_date"))
    rating = models.FloatField(
        _("rating"),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(
        _("type"), max_length=20, choices=ContentType.choices
    )
    genres = models.ManyToManyField("Genre", through="GenreFilmWork")
    persons = models.ManyToManyField("Person", through="PersonFilmWork")

    # permissions = models.ManyToManyField(
    #     "Permission", through="PermissionFilmWork"
    # )

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("film_work")
        verbose_name_plural = _("film_works")
        ordering = ["-creation_date"]
        unique_together = (("title", "creation_date"),)

    def __str__(self):
        return self.title


# class PermissionFilmWork(UUIDMixin, CreatedMixin):
#     film_work = models.ForeignKey("FilmWork", on_delete=models.CASCADE)
#     permission = models.ForeignKey(
#         "Permission", on_delete=models.CASCADE, verbose_name="permission"
#     )
#
#     class Meta:
#         db_table = 'access"."permission_film_work'
#         verbose_name = "permission_film_work"
#         verbose_name_plural = "permission_film_works"
#         unique_together = ("film_work", "permission")


class Genre(TimeStampedMixin, UUIDMixin, DescriptionMixin):
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")
        ordering = ["name"]

    def __str__(self):
        return self.name


class GenreFilmWork(UUIDMixin, CreatedMixin):
    film_work = models.ForeignKey("FilmWork", on_delete=models.CASCADE)
    genre = models.ForeignKey(
        "Genre", on_delete=models.CASCADE, verbose_name=_("genre")
    )

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("genre_film_work")
        verbose_name_plural = _("genre_film_works")
        unique_together = ("film_work", "genre")


class Person(TimeStampedMixin, UUIDMixin):
    full_name = models.CharField(_("full_name"), max_length=25)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("person")
        verbose_name_plural = _("persons")
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class PersonFilmWork(UUIDMixin, CreatedMixin):
    class RoleType(models.TextChoices):
        ACTOR = "actor", _("actor")
        DIRECTOR = "director", _("director")
        WRITER = "writer", _("writer")

    film_work = models.ForeignKey("FilmWork", on_delete=models.CASCADE)
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, verbose_name=_("person")
    )
    role = models.CharField(_("type"), max_length=20, choices=RoleType.choices)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _("person_film_work")
        verbose_name_plural = _("person_film_works")
        unique_together = ("film_work", "person", "role")
