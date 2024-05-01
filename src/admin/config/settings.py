from pathlib import Path

from split_settings.tools import include
from core.configs.django import settings as django_settings

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = django_settings.secret_key.get_secret_value()
DEBUG = django_settings.get_debug
ALLOWED_HOSTS = django_settings.get_allowed_hosts

include(
    "components/apps.py",
    "components/middleware.py",
    "components/templates.py",
    "components/database.py",
    "components/auth.py",
)

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "ru-RU"

LOCALE_PATHS = ["movies/locale"]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "collected_static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
