import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import MyUserManager


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        max_length=64,
        unique=True,
        verbose_name="email",
        help_text="Введите email",
    )
    first_name = models.CharField(
        max_length=64,
        verbose_name="имя пользователя",
        help_text="Введите имя",
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=64,
        verbose_name="фамилия пользователя",
        help_text="Введите фамилию",
        blank=True,
        null=True,
    )
    is_staff = models.BooleanField(default=False)

    class Meta:
        db_table = "users"
        ordering = ["email"]
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} {self.id}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
