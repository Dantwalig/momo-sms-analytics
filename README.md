# MoMo SMS Analytics

## Team Members

- Abdul Kudus Zakaria Mukhtaru
- Ariane Itetero
- Modupe Akanni
- Peter Mfitumukiza
- Daniel Gakumba Ntwali

## Project Description

This project processes MoMo (Mobile Money) SMS data in XML format, cleans and categorizes the data, stores it in a relational database, and provides a frontend interface to analyze and visualize the data. The application demonstrates enterprise-level fullstack development with backend data processing, database management, and frontend development.

## Project Structure

```
.
├── README.md                         # Setup, run, overview
├── .env.example                      # DATABASE_URL or path to SQLite
├── requirements.txt                  # Python dependencies
├── index.html                        # Dashboard entry (static)
├── web/
│   ├── styles.css                    # Dashboard styling
│   ├── chart_handler.js              # Fetch + render charts/tables
│   └── assets/                       # Images/icons (optional)
├── data/
│   ├── raw/                          # Provided XML input (git-ignored)
│   │   └── momo.xml
│   ├── processed/                    # Cleaned/derived outputs for frontend
│   │   └── dashboard.json            # Aggregates the dashboard reads
│   ├── db.sqlite3                    # SQLite DB file
│   └── logs/
│       ├── etl.log                   # Structured ETL logs
│       └── dead_letter/              # Unparsed/ignored XML snippets
├── etl/
│   ├── __init__.py
│   ├── config.py                     # File paths, thresholds, categories
│   ├── parse_xml.py                  # XML parsing (ElementTree/lxml)
│   ├── clean_normalize.py            # Amounts, dates, phone normalization
│   ├── categorize.py                 # Simple rules for transaction types
│   ├── load_db.py                    # Create tables + upsert to SQLite
│   └── run.py                        # CLI: parse -> clean -> categorize -> load -> export JSON
├── api/                              # Optional (bonus)
│   ├── __init__.py
│   ├── app.py                        # Minimal FastAPI with /transactions, /analytics
│   ├── db.py                         # SQLite connection helpers
│   └── schemas.py                    # Pydantic response models
├── scripts/
│   ├── run_etl.sh                    # python etl/run.py --xml data/raw/momo.xml
│   ├── export_json.sh                # Rebuild data/processed/dashboard.json
│   └── serve_frontend.sh             # python -m http.server 8000 (or Flask static)
└── tests/
    ├── test_parse_xml.py             # Small unit tests
    ├── test_clean_normalize.py
    └── test_categorize.py
```

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd momo-sms-analytics
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```

5. Place your XML data file in `data/raw/momo.xml`

## Usage

### Run ETL Pipeline

Process the XML data through the ETL pipeline:
```bash
bash scripts/run_etl.sh
# Or specify a custom XML file:
bash scripts/run_etl.sh path/to/your/file.xml
```

Or directly:
```bash
python etl/run.py --xml data/raw/momo.xml
```

### Export Dashboard JSON

Rebuild the dashboard JSON file:
```bash
bash scripts/export_json.sh
```

### Serve Frontend

Start the frontend server:
```bash
bash scripts/serve_frontend.sh
# Or specify a custom port:
bash scripts/serve_frontend.sh 8080
```

Then open `http://localhost:8000` in your browser.

### Run Tests

```bash
python -m pytest tests/
# Or
python -m unittest discover tests
```

## Development Workflow

1. **ETL Pipeline**: The ETL pipeline processes XML data through these steps:
   - Parse XML file
   - Clean and normalize data (amounts, dates, phone numbers)
   - Categorize transactions
   - Load into SQLite database
   - Export aggregated JSON for dashboard

2. **Frontend**: The dashboard reads from `data/processed/dashboard.json` and visualizes:
   - Summary statistics
   - Transaction charts (by category, over time)
   - Transaction table

3. **API** (Optional/Bonus): FastAPI endpoints for serving transaction data and analytics

## Notes

- Raw XML files in `data/raw/` are git-ignored
- Database files (`*.sqlite3`) are git-ignored
- Logs are stored in `data/logs/`
- Unparsed XML snippets are stored in `data/logs/dead_letter/`
