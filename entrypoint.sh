#!/bin/sh

  while ! nc -z db 5432; do
    sleep 0.1
  done

bash -c "python manage.py collectstatic --noinput"
bash -c "python manage.py makemigrations"
bash -c "python manage.py migrate"
bash -c "python manage.py loaddata fixture.json"
exec "$@"
