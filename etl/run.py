"""
Main ETL pipeline runner.
Orchestrates: parse -> clean -> categorize -> load -> export JSON
"""

import argparse
import json
import logging
from pathlib import Path
from etl.config import (
    RAW_XML_PATH,
    PROCESSED_JSON_PATH,
    DATABASE_PATH,
    ETL_LOG_PATH
)
from etl.parse_xml import parse_xml_file
from etl.clean_normalize import clean_transaction
from etl.categorize import apply_categorization
from etl.load_db import load_to_database


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(ETL_LOG_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def export_dashboard_json(transactions: list, output_path: str) -> None:
    """
    Export aggregated data for dashboard visualization.
    
    Args:
        transactions: List of processed transactions
        output_path: Path to output JSON file
    """
    # TODO: Aggregate data for dashboard
    # Calculate totals by category, date ranges, etc.
    # Export to JSON format
    pass


def run_etl_pipeline(xml_path: str) -> None:
    """
    Run the complete ETL pipeline.
    
    Args:
        xml_path: Path to input XML file
    """
    logger.info(f"Starting ETL pipeline for {xml_path}")
    
    # Step 1: Parse XML
    logger.info("Parsing XML file...")
    transactions = parse_xml_file(xml_path)
    logger.info(f"Parsed {len(transactions)} transactions")
    
    # Step 2: Clean and normalize
    logger.info("Cleaning and normalizing data...")
    cleaned_transactions = [clean_transaction(t) for t in transactions]
    
    # Step 3: Categorize
    logger.info("Categorizing transactions...")
    categorized_transactions = apply_categorization(cleaned_transactions)
    
    # Step 4: Load to database
    logger.info("Loading to database...")
    load_to_database(categorized_transactions)
    
    # Step 5: Export dashboard JSON
    logger.info("Exporting dashboard JSON...")
    export_dashboard_json(categorized_transactions, PROCESSED_JSON_PATH)
    
    logger.info("ETL pipeline completed successfully")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Run ETL pipeline for MoMo SMS data")
    parser.add_argument(
        "--xml",
        type=str,
        default=RAW_XML_PATH,
        help="Path to input XML file"
    )
    args = parser.parse_args()
    
    # Ensure output directories exist
    Path(PROCESSED_JSON_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(ETL_LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
    
    run_etl_pipeline(args.xml)


if __name__ == "__main__":
    main()

