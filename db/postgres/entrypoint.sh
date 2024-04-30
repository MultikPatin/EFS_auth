#!/bin/bash

echo "------------------------START_INIT_DB-------------------"

psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f docker-entrypoint-initdb.d/movies_database.ddl

echo "------------------------END_INIT_DB---------------------"
