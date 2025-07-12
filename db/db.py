import os

from dotenv import load_dotenv
from psycopg2 import pool

from utils.logger import get_logger

logger = get_logger(__name__)
load_dotenv()

connection_pool = None

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "muse_observatory"),
    "user": os.getenv("DB_USER", "museuser"),
    "password": os.getenv("DB_PASSWORD", "musepassword"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}


def init_db_pool():
    global connection_pool
    try:
        connection_pool = pool.SimpleConnectionPool(minconn=1, maxconn=10, **DB_CONFIG)
        logger.info("Database connection pool initialized")
    except Exception as e:
        logger.error(f"Error initializing connection pool: {e}")
        raise


def get_db_connection():
    if not connection_pool:
        init_db_pool()
    return connection_pool.getconn()


def return_db_connection(conn: str):
    if connection_pool:
        connection_pool.putconn(conn)


def close_db_pool():
    if connection_pool:
        connection_pool.closeall()
        logger.info("Database connection pool closed")
