import psycopg2
from psycopg2.extensions import connection

DB_CONFIG = {
    "dbname": "employees_db",
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}


def get_connection() -> connection:
    return psycopg2.connect(**DB_CONFIG)
