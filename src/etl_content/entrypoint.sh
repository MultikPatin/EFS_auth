export PYTHONPATH=$SRC_PATH
rm poetry.lock
rm pyproject.toml
cd "$APP_DIR" || exit
rm Dockerfile
python main.py
