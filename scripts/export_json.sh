#!/bin/bash
# Rebuild dashboard JSON from database

# Run ETL to regenerate dashboard.json
python etl/run.py --xml data/raw/momo.xml

echo "Dashboard JSON exported to data/processed/dashboard.json"

