#!/bin/bash

echo "Iniciando script de arranque..."

# Salir si algún comando falla
set -e

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
exec gunicorn DEFCON5.wsgi:application --bind 0.0.0.0:8000 --workers 3
