#!/usr/bin/env bash

gunicorn -w $PWPWORKERS --bind :8000 app_flask:app
