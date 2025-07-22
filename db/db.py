import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
from tinydb import Query, TinyDB

from utils.logger import get_logger

logger = get_logger(__name__)
load_dotenv()

# Database file paths
DB_DIR = Path(os.getenv("DB_DIR", "db_files"))
DB_FILE = DB_DIR / "muse_observatory.json"

# Database instances (lazy-loaded)
_db_instance = None


def get_db() -> TinyDB:
    """Get the TinyDB database instance."""
    global _db_instance
    if _db_instance is None:
        logger.info("No instance of TinyDB found, initializing...")
        try:
            # Ensure directory exists with proper permissions
            try:
                DB_DIR.mkdir(exist_ok=True)
                logger.info(f"Database directory initialized at {DB_DIR}")
                # Attempt to make the directory writable if it exists but isn't writable
                if DB_DIR.exists() and not os.access(DB_DIR, os.W_OK):
                    os.chmod(DB_DIR, 0o777)
                    logger.info(f"Updated permissions for {DB_DIR}")
            except PermissionError:
                logger.error(
                    f"Permission denied: Cannot create or modify directory {DB_DIR}"
                )
                logger.info(
                    "Trying to continue anyway, in case the database file is already accessible"
                )

            # Try to open or create the database file
            try:
                _db_instance = TinyDB(DB_FILE)
                logger.info(f"TinyDB initialized at {DB_FILE}")

                # Log database file existence and tables
                if os.path.exists(DB_FILE):
                    file_size = os.path.getsize(DB_FILE)
                    logger.info(f"Database file exists with size: {file_size} bytes")

                    # Log tables and record counts
                    tables = _db_instance.tables()
                    logger.info(f"Available tables: {tables}")
                    for table_name in tables:
                        table = _db_instance.table(table_name)
                        logger.info(f"Table '{table_name}' has {len(table)} records")
                else:
                    logger.warning(f"Database file doesn't exist yet: {DB_FILE}")

            except PermissionError:
                error_msg = f"Permission denied: Cannot write to {DB_FILE}. Check that the application has proper permissions."
                logger.error(error_msg)
                raise PermissionError(error_msg)
        except Exception as e:
            logger.error(f"Error initializing TinyDB: {e}")
            raise
    return _db_instance


def init_db_pool():
    """Initialize database - ensures db directory exists"""
    try:
        # Create DB directory if it doesn't exist
        try:
            DB_DIR.mkdir(exist_ok=True)
            logger.info(f"Database directory initialized at {DB_DIR}")
        except PermissionError:
            logger.error(f"Permission denied: Cannot create directory {DB_DIR}")

        # Initialize DB connection (lazy loading)
        db = get_db()
        logger.info("Database initialized")

        # Log database content info after initialization
        tables = db.tables()
        if not tables:
            logger.warning(
                "No tables found in the database. This is normal for a fresh installation."
            )
        else:
            logger.info(f"Database contains {len(tables)} tables: {tables}")
            for table_name in tables:
                table = db.table(table_name)
                logger.info(f"Table '{table_name}' has {len(table)} records")

    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


# Legacy compatibility functions for older code
def get_db_connection():
    """Get the database instance (compatibility with old code)"""
    return get_db()


def return_db_connection(conn: TinyDB) -> None:
    """No-op function for compatibility with old code"""
    pass


# Helper functions for data operations with logging
def insert_with_logging(table_name: str, data: dict) -> int:
    """Insert data into a table with detailed logging"""
    db = get_db()
    table = db.table(table_name)

    # Log the operation
    logger.info(f"Inserting data into '{table_name}' table")
    logger.debug(f"Data to insert: {data}")

    # Perform the insert
    doc_id = table.insert(data)

    # Log the result
    logger.info(f"Successfully inserted document with ID {doc_id} into '{table_name}'")
    logger.info(f"Table '{table_name}' now has {len(table)} records")

    return doc_id


def search_with_logging(
    table_name: str, query: Union[Query, Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Search data with detailed logging"""
    db = get_db()
    table = db.table(table_name)

    # Log the operation
    logger.info(f"Searching in '{table_name}' table with query: {query}")

    # Perform the search
    results = table.search(query)

    # Log the results
    logger.info(f"Found {len(results)} matching records in '{table_name}'")
    if not results:
        logger.warning(f"No matching records found in '{table_name}'")

    return results


def get_with_logging(
    table_name: str, query: Union[Query, Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Get a single record with detailed logging"""
    db = get_db()
    table = db.table(table_name)

    # Log the operation
    logger.info(f"Getting a record from '{table_name}' table with query: {query}")

    # Perform the get
    result = table.get(query)

    # Log the result
    if result:
        logger.info(f"Successfully retrieved a record from '{table_name}'")
        logger.debug(f"Retrieved data: {result}")
    else:
        logger.warning(f"No matching record found in '{table_name}'")

    return result
