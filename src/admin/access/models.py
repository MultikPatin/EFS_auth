import uuid

from django.db import models


class DescriptionMixin(models.Model):
    description = models.TextField(
        "description", blank=True, null=True, max_length=255
    )

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.TextField("name", unique=True, max_length=64)

    class Meta:
        abstract = True


class CreatedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TimeStampedMixin(CreatedMixin):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        abstract = True


class Role(TimeStampedMixin, UUIDMixin, DescriptionMixin, NameMixin):
    class Meta:
        db_table = 'public"."roles'
        verbose_name = "role"
        verbose_name_plural = "roles"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Permission(TimeStampedMixin, UUIDMixin, DescriptionMixin, NameMixin):
    class Meta:
        db_table = 'public"."permissions'
        verbose_name = "permission"
        verbose_name_plural = "permissions"
        ordering = ["name"]

    def __str__(self):
        return self.name
