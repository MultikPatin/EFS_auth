FROM python:3.11-slim

ENV SRC_PATH '/app'
ENV APP_DIR 'src/etl_permission'

WORKDIR $SRC_PATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.create false \
    && poetry install --extras etl_permission --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY ./${APP_DIR} ./${APP_DIR}
COPY ./src/core/__init__.py ./src/core/__init__.py
COPY ./src/core/configs ./src/core/configs
COPY ./src/core/utils/__init__.py ./src/core/utils/__init__.py
COPY ./src/core/utils/logger.py ./src/core/utils/logger.py

RUN chmod +x ${APP_DIR}/entrypoint.sh

ENTRYPOINT ["/bin/bash", "-c", "exec ${SRC_PATH}/${APP_DIR}/entrypoint.sh"]
