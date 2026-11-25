#!/bin/sh
set -e
python -m app.infrastructure.migrate
exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 "app.main:wsgi()"
