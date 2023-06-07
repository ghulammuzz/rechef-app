#!/bin/bash
python3 -m venv env
source env/bin/activate
pip install djangorestframework djangorestframework-simplejwt pillow
django-admin startproject django_app .
echo "env" > .gitignore
