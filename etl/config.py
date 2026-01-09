"""
Configuration file for ETL pipeline.
Contains file paths, thresholds, and categorization rules.
"""

# File paths
RAW_XML_PATH = "data/raw/momo.xml"
PROCESSED_JSON_PATH = "data/processed/dashboard.json"
DATABASE_PATH = "data/db.sqlite3"
LOG_DIR = "data/logs"
ETL_LOG_PATH = "data/logs/etl.log"
DEAD_LETTER_DIR = "data/logs/dead_letter"

# Processing thresholds
MIN_AMOUNT = 0
MAX_AMOUNT = 100000000  # Adjust based on your data

# Transaction categories
TRANSACTION_CATEGORIES = {
    "deposit": ["deposit", "received", "credit"],
    "withdrawal": ["withdrawal", "sent", "debit", "payment"],
    "transfer": ["transfer", "sent to", "received from"],
    "purchase": ["purchase", "paid", "bought"],
    "other": []  # Default category
}

