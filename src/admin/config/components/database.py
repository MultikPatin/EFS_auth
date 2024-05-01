from core.configs.postgres import settings as postgres_settings

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": postgres_settings.db_name,
        "USER": postgres_settings.user,
        "PASSWORD": postgres_settings.password.get_secret_value(),
        "HOST": postgres_settings.host,
        "PORT": postgres_settings.port,
        "OPTIONS": {"options": "-c search_path=public,content"},
    }
}
