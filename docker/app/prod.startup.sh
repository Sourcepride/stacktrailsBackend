#!/bin/sh
echo "Running migrations.."

python manage.py migrate

echo "collecting static files"

python manage.py collectstatic --no-input

uwsgi --ini app.ini