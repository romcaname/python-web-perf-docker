#!/usr/bin/env bash

uvicorn --host 0.0.0.0 --port 8000 --workers $PWPWORKERS app_starlette:app
