#!/usr/bin/env bash

python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input

exec "$@"
