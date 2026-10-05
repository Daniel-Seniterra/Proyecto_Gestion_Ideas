import os
from urllib.parse import urlparse
from flask import g


def get_db():
    if "db" not in g:
        database_url = os.getenv("DATABASE_URL")

        if database_url and database_url.startswith(("postgres://", "postgresql://")):
            import psycopg2
            import psycopg2.extras

            if database_url.startswith("postgres://"):
                database_url = database_url.replace("postgres://", "postgresql://", 1)

            g.db = psycopg2.connect(
                database_url,
                cursor_factory=psycopg2.extras.RealDictCursor
            )
        else:
            import pymysql
            import pymysql.cursors

            g.db = pymysql.connect(
                host=os.getenv("MYSQL_HOST", "localhost"),
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", ""),
                database=os.getenv("MYSQL_DATABASE", "gestion_ideas"),
                port=int(os.getenv("MYSQL_PORT", "3306")),
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )

    return g.db


def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
