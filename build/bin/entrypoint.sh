#!/bin/sh

. ~/.bashrc

pip install -e .

if [ "$DATABASE" = "{database_name}" ]; then
  echo "Waiting for {database_name}..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi


manage run -h 0.0.0.0