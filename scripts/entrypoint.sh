#!/bin/sh

if [ "$ENV" = "prod" ]; then
    exec gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
else
    exec uvicorn main:app --host 0.0.0.0 --port 80 --reload
fi