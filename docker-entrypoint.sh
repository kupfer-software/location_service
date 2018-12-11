#!/bin/bash

# It is responsability of the deployment orchestration to execute before
# migrations, create default admin user, populate minimal data, etc.

gunicorn location_service.wsgi --config location_service/gunicorn_conf.py
