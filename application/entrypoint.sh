#!/bin/sh
CONTAINER_ALREADY_STARTED="CONTAINER_ALREADY_STARTED_PLACEHOLDER"
python3 pay_parking/manage.py makemigrations
python3 pay_parking/manage.py migrate
if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    touch $CONTAINER_ALREADY_STARTED
    python3 pay_parking/manage.py import pay_parking/db.json 
fi
python3 pay_parking/manage.py collectstatic
cp -r /app/pay_parking/collected_static/. /backend_static/static/
python3 pay_parking/manage.py runserver 0.0.0.0:${APP_PORT}