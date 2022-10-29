#!/bin/bash

set -e

echo "Migrating Database"


echo "Starting application"

export PYTHONPATH="${PYTHONPATH}:/opt/app/"
gunicorn --bind 0.0.0.0:8010 --workers 3 project_shopply.wsgi:application