#!/usr/bin/env bash

gunicorn -w 50 --bind :8001 external_app_flask:app
