#!/bin/bash
# Run ETL pipeline script

# Default XML path
XML_PATH="${1:-data/raw/momo.xml}"

# Run the ETL pipeline
python etl/run.py --xml "$XML_PATH"

echo "ETL pipeline completed. Check data/logs/etl.log for details."

