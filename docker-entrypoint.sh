#!/bin/bash

bash scripts/tcp-port-wait.sh $${DATABASE_HOST} $${DATABASE_PORT}

python manage.py migrate

gunicorn location_service.wsgi --config location_service/gunicorn_conf.py
