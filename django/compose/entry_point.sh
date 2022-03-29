#!/usr/bin/env bash

$(/wait-for-it.sh db:3306) && python manage.py runserver 0.0.0.0:8080
