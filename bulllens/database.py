"""
Database connection and configuration for BullLens FastAPI backend.
Uses mysql-connector-python with configuration via .env variables.
"""

import os
from mysql.connector import connect, Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()


def get_db_config() -> dict:
    """
    Load database configuration from environment variables.
    Returns a dict compatible with mysql.connector.connect().
    """
    return {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "root"),
        "database": os.getenv("DB_NAME", "bulllens_db"),
        "autocommit": False,
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
    }


def get_connection() -> MySQLConnectionAbstract:
    """
    Establish a new MySQL connection using configuration from .env.
    
    Returns:
        MySQLConnectionAbstract: Active database connection with DictCursor.
    
    Raises:
        Error: If connection fails (e.g., database not running, wrong credentials).
    """
    try:
        conn = connect(**get_db_config())
        return conn
    except Error as e:
        raise Error(f"Database connection failed: {e}")


@contextmanager
def get_db_cursor(commit: bool = True):
    """
    Context manager for database operations.
    Automatically handles connection, cursor creation, and cleanup.
    
    Usage:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            rows = cursor.fetchall()
    
    Args:
        commit: If True, commits on success; if False, rolls back.
    
    Yields:
        cursor: MySQLCursor with dictionary row factory.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        yield cursor
        if commit:
            conn.commit()
        else:
            conn.rollback()
    except Error as e:
        if conn:
            conn.rollback()
        raise Error(f"Database operation failed: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()


def init_db() -> None:
    """
    Initialize database schema by executing schema.sql if tables don't exist.
    This is called by the FastAPI startup event.
    """
    schema_path = os.path.join(os.path.dirname(__file__), "sql", "schema.sql")
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    conn = None
    try:
        with open(schema_path, "r") as f:
            schema_sql = f.read()
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Execute schema statements (split by ;)
        for statement in schema_sql.split(";"):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        
        conn.commit()
        print("✓ Database schema initialized successfully")
    except Error as e:
        raise Error(f"Schema initialization failed: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
