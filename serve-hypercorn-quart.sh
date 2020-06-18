#!/usr/bin/env bash

hypercorn -w $PWPWORKERS --bind :8000 app_quart:app
