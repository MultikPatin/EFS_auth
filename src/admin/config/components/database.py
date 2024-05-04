from src.admin.core.config import settings

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.postgres_content.database,
        "USER": settings.postgres_content.user,
        "PASSWORD": settings.postgres_content.password.get_secret_value(),
        "HOST": settings.postgres_content.host,
        "PORT": settings.postgres_content.port,
        "OPTIONS": {"options": "-c search_path=public,content"},
    }
}
