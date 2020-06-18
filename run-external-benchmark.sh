#!/usr/bin/env bash

CONCURRENCY=15
REQUEST_COUNT=50

ab -c $CONCURRENCY -n $REQUEST_COUNT http://backend_service:8000/external-test >current_run.txt 2>&1
