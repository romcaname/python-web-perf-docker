#!/usr/bin/env bash

uvicorn -w $PWPWORKERS --bind :8000 app_flask:app
