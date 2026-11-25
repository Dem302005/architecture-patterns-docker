import time

import psycopg2


def connect(settings, retries=30, delay=1.0):
    last_error = None
    for _ in range(retries):
        try:
            return psycopg2.connect(
                host=settings.db_host,
                port=settings.db_port,
                dbname=settings.db_name,
                user=settings.db_user,
                password=settings.db_pass,
            )
        except psycopg2.OperationalError as error:
            last_error = error
            time.sleep(delay)
    raise last_error
