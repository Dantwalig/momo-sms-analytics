"""
Configuration module for API.
Contains database connection settings and authentication credentials.
"""

import os
from typing import Dict, Any

# Database configuration
DB_CONFIG: Dict[str, Any] = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'momo-sms-analytics'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'charset': 'utf8mb4',
    'autocommit': False
}

# Basic Authentication credentials
AUTH_USERNAME = os.getenv('API_USERNAME', 'admin')
AUTH_PASSWORD = os.getenv('API_PASSWORD', 'password')

# Server configuration
SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
SERVER_PORT = int(os.getenv('SERVER_PORT', 8000))
