# Команды

### Poetry

- Установка зависимостей для всех проектов:
   ```bash
  poetry install --all-extras --with dev --with test
  ```

### Pre-commit

- Install the git hook scripts:
  ```bash
  pre-commit install
  ```
- Run against all the files:
  ```bash
  pre-commit run --all-files
  ```

### Alembic

- Создание миграции:
  ```bash
  alembic revision --autogenerate -m "<название миграции>"
  ```
- Применить все ревизии базы:
  ```bash
  alembic upgrade head
  ```
- Применить конкретную ревизии базы:
  ```bash
  alembic upgrade <ревизия>
  ```
- Вывести текущую ревизию базы данных:
  ```bash
  alembic current
  ```
- Вывести список доступных ревизий базы данных:
  ```bash
  alembic show
  ```
- Откатить все ревизии базы данных:
  ```bash
  alembic downgrade base
  ```
- Откатить до конкретной ревизии базы данных:
  ```bash
  alembic downgrade <ревизия>
  ```
