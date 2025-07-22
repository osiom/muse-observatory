import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from tinydb import Query, TinyDB

from utils.logger import get_logger

logger = get_logger(__name__)
load_dotenv()

# Database file paths
DB_DIR = Path(os.getenv("DB_DIR", "db_files"))
DB_FILE = DB_DIR / "muse_observatory.json"

# Ensure DB directory exists
DB_DIR.mkdir(exist_ok=True)

# Database instances (lazy-loaded)
_db_instance = None


def get_db() -> TinyDB:
    """Get the TinyDB database instance."""
    global _db_instance
    if _db_instance is None:
        try:
            _db_instance = TinyDB(DB_FILE)
            logger.info(f"TinyDB initialized at {DB_FILE}")
        except Exception as e:
            logger.error(f"Error initializing TinyDB: {e}")
            raise
    return _db_instance


def init_db_pool():
    """Initialize database - ensures db directory exists"""
    try:
        # Create DB directory if it doesn't exist
        DB_DIR.mkdir(exist_ok=True)
        # Initialize DB connection (lazy loading)
        _ = get_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


def get_db_connection():
    """Get the database instance (compatibility with old code)"""
    return get_db()


def return_db_connection(conn: any) -> None:
    """No-op function for compatibility with old code"""
    pass


def close_db_pool():
    """Close the database connection"""
    global _db_instance
    if _db_instance:
        _db_instance.close()
        _db_instance = None
        logger.info("Database connection closed")
