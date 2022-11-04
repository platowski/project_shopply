#!/bin/bash

set -e

export PYTHONPATH="${PYTHONPATH}:/opt/app/"
echo "Migrating Database"
python manage.py migrate

echo "Collecting Statics"
#python manage.py collectstatic

echo "Starting application"
gunicorn --bind 0.0.0.0:8010 --workers 1 project_shopply.wsgi:application