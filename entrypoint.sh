#!/bin/bash
while !</dev/tcp/db/5432; do sleep 1; done;

python3 manage.py create_tables

python3 manage.py createsuperuserauto
# gunicorn main:app -c gunicorn.config.py
uvicorn main:app --reload --host 0.0.0.0
