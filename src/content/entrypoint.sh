export PYTHONPATH=$SRC_PATH
rm poetry.lock
rm pyproject.toml
cd "$APP_DIR" || exit
rm Dockerfile
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind "$CONTENT_API_HOST":"$CONTENT_API_PORT"
#
