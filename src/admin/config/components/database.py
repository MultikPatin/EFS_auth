from src.admin.core.config import settings

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.postgres_content.database,
        "USER": settings.postgres_content.user,
        "PASSWORD": settings.postgres_content.password.get_secret_value(),
        "HOST": settings.postgres_content.correct_host(),
        "PORT": settings.postgres_content.correct_port(),
        "OPTIONS": {"options": "-c search_path=public,content"},
    },
    "auth": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.postgres_auth.database,
        "USER": settings.postgres_auth.user,
        "PASSWORD": settings.postgres_auth.password.get_secret_value(),
        "HOST": settings.postgres_auth.correct_host(),
        "PORT": settings.postgres_auth.correct_port(),
        "OPTIONS": {"options": "-c search_path=public,auth"},
    },
}
