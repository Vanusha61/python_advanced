#!/bin/sh
set -e

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting Gunicorn..."
exec gunicorn -w 4 -b 0.0.0.0:8000 run:app