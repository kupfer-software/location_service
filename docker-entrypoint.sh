#!/bin/bash

python manage.py migrate

gunicorn location_service.wsgi --config location_service/gunicorn_conf.py
