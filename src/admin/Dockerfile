FROM python:3.11

ENV SRC_PATH '/opt/app'
ENV APP_DIR 'django_api'

WORKDIR $SRC_PATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'


COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.create false \
    && poetry install --extras django_api --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY ./${APP_DIR} ./${APP_DIR}
COPY ./core/configs/__init__.py ./core/configs/__init__.py
COPY ./core/configs/django.py ./core/configs/django.py
COPY ./core/configs/postgres.py ./core/configs/postgres.py

RUN chmod +x ${APP_DIR}/entrypoint.sh

ENTRYPOINT ["/bin/bash", "-c", "exec ${SRC_PATH}/${APP_DIR}/entrypoint.sh"]
