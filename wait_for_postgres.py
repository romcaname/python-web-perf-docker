import os
import logging
from time import time, sleep
import psycopg2
import re
import urllib.parse

check_timeout = int(os.getenv("POSTGRES_CHECK_TIMEOUT", 30))
check_interval = int(os.getenv("POSTGRES_CHECK_INTERVAL", 1))
interval_unit = "second" if check_interval == 1 else "seconds"

CORE_POSTGRES_DB = os.getenv('CORE_POSTGRES_DB', 'test')
CORE_POSTGRES_PORT = os.getenv('CORE_POSTGRES_PORT', 5432)
CORE_POSTGRES_PASS = os.getenv('CORE_POSTGRES_PASS', 'test')
CORE_POSTGRES_USER = os.getenv('CORE_POSTGRES_USER', 'test')
CORE_POSTGRES_HOST = os.getenv('CORE_POSTGRES_HOST', 'db')

config = {
    "dbname": CORE_POSTGRES_DB,
    "user": CORE_POSTGRES_USER,
    "password": CORE_POSTGRES_PASS,
    "host": CORE_POSTGRES_HOST
}

start_time = time()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def pg_isready(host, user, password, dbname):
    while time() - start_time < check_timeout:
        try:
            conn = psycopg2.connect(**vars())
            logger.info("Postgres is ready! ✨ 💅")
            conn.close()
            return True
        except psycopg2.OperationalError:
            logger.info(f"Postgres isn't ready. Waiting for {check_interval} {interval_unit}...")
            sleep(check_interval)

    logger.error(f"We could not connect to Postgres within {check_timeout} seconds.")
    return False


pg_isready(**config)