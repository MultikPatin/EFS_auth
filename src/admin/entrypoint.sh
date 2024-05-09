export PYTHONPATH=$SRC_PATH
rm poetry.lock
rm pyproject.toml
cd "$APP_DIR"/
python manage.py migrate movies --fake
python manage.py migrate access --database=auth_db --fake
python manage.py migrate
python manage.py collectstatic --clear --noinput
cp -r "$SRC_PATH"/"$APP_DIR"/collected_static/. /backend_static/static/
python manage.py init_superuser --no-input
set -e
chown www-data:www-data /var/log
rm Dockerfile
uwsgi --strict --ini "$SRC_PATH"/"$APP_DIR"/uwsgi.ini
