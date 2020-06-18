#!/usr/bin/env bash

gunicorn -w 30 --bind :8001 external_app_flask:app
