from src.admin.core.config import settings

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.postgres.database,
        "USER": settings.postgres.user,
        "PASSWORD": settings.postgres.password.get_secret_value(),
        "HOST": settings.postgres.host,
        "PORT": settings.postgres.port,
        "OPTIONS": {"options": "-c search_path=public,content"},
    }
}
