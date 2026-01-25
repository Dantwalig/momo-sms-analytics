"""
Database connection helpers for API.
"""

import mysql.connector
from mysql.connector import Error
from typing import Optional
from contextlib import contextmanager
from api.config import DB_CONFIG


@contextmanager
def get_db_connection():
    """
    Get MySQL database connection as a context manager.
    Automatically handles connection closing and error handling.
    
    Yields:
        mysql.connector.MySQLConnection object
        
    Raises:
        Error: If connection fails
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn and conn.is_connected():
            conn.close()


def get_db_connection_simple():
    """
    Get MySQL database connection (simple version without context manager).
    Caller is responsible for closing the connection.
    
    Returns:
        mysql.connector.MySQLConnection object
        
    Raises:
        Error: If connection fails
    """
    return mysql.connector.connect(**DB_CONFIG)

