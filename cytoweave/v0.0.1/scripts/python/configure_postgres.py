import os
import psycopg2


def configure_postgres_connection():

    if os.getenv("PGDATABASE") is None:
        raise ValueError("PGDATABASE must be set")
    pg_database = os.getenv("PGDATABASE")

    if os.getenv("PGUSER") is None:
        raise ValueError("PGUSER must be set")
    pg_user = os.getenv("PGUSER")

    if os.getenv("PGPASSWORD") is None:
        raise ValueError("PGPASSWORD must be set")
    pg_password = os.getenv("PGPASSWORD")

    if os.getenv("PGHOST") is None:
        raise ValueError("PGHOST must be set")
    pg_host = os.getenv("PGHOST")

    if os.getenv("PGPORT") is None:
        raise ValueError("PGPORT must be set")
    pg_port = os.getenv("PGPORT")

    conn = psycopg2.connect(
        dbname=pg_database,
        user=pg_user,
        host=pg_host,
        password=pg_password,
        port=pg_port
    )
    conn.autocommit = True

    return conn
