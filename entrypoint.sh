#!/bin/bash
# make migrations
python manage.py makemigrations
# run migrations
python manage.py migrate
# run django server
python manage.py runserver 0.0.0.0:8000