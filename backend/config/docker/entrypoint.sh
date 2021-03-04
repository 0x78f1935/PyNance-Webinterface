#!/bin/sh

export FLASK_APP=webserver.py

while ! curl -o - database:3306; do sleep 1; done

{
    flask db init
} || {
    echo 'Database already initialized'
}
flask db migrate
flask db upgrade

# flask run
gunicorn --bind 0.0.0.0:5000 --error-logfile - --access-logfile - --capture-output --worker-tmp-dir /dev/shm --log-level=debug --workers=1 --timeout 200 'webserver:create_server()'