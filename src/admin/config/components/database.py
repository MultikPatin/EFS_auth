from django.conf import settings

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.ADVANCED_SETTINGS.postgres_content.database,
        "USER": settings.ADVANCED_SETTINGS.postgres_content.user,
        "PASSWORD": settings.ADVANCED_SETTINGS.postgres_content.password.get_secret_value(),
        "HOST": settings.ADVANCED_SETTINGS.postgres_content.correct_host(),
        "PORT": settings.ADVANCED_SETTINGS.postgres_content.correct_port(),
        "OPTIONS": {"options": "-c search_path=public,content,access"},
    },
    "auth_db": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.ADVANCED_SETTINGS.postgres_auth.database,
        "USER": settings.ADVANCED_SETTINGS.postgres_auth.user,
        "PASSWORD": settings.ADVANCED_SETTINGS.postgres_auth.password.get_secret_value(),
        "HOST": settings.ADVANCED_SETTINGS.postgres_auth.correct_host(),
        "PORT": settings.ADVANCED_SETTINGS.postgres_auth.correct_port(),
        "OPTIONS": {"options": "-c search_path=public,auth"},
    },
}
