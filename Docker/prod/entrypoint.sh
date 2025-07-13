#!/bin/sh
set -e

# Migrações
python manage.py migrate --noinput

# Coleta estáticos
python manage.py collectstatic --noinput

# Inicia gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4 \

