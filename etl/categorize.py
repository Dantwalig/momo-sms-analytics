"""
Transaction categorization module.
Uses simple rule-based approach to categorize transactions.
"""

from typing import Dict, Any
from etl.config import TRANSACTION_CATEGORIES


def categorize_transaction(transaction: Dict[str, Any]) -> str:
    """
    Categorize a transaction based on message content and patterns.
    
    Args:
        transaction: Transaction dictionary with message/content field
        
    Returns:
        Category string (e.g., "deposit", "withdrawal", "transfer", etc.)
    """
    # TODO: Implement categorization logic
    # Check message content against TRANSACTION_CATEGORIES
    # Return appropriate category or "other" as default
    pass


def apply_categorization(transactions: list) -> list:
    """
    Apply categorization to a list of transactions.
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        List of transactions with category field added
    """
    # TODO: Apply categorize_transaction to each transaction
    pass

