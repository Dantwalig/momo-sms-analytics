# MoMo SMS Analytics

## Team Members

* Abdul Kudus Zakaria Mukhtaru
* Ariane Itetero
* Modupe Akanni
* Peter Mfitumukiza
* Daniel Gakumba Ntwali

## Project Description

This project processes MoMo (Mobile Money) SMS data in XML format, cleans and categorizes the data, stores it in a relational database, and provides a REST API for secure data access. The application demonstrates enterprise-level fullstack development with backend data processing, database management, API security, and efficient data structure implementation.

The project includes:
- **Week 1-2**: ETL pipeline, database design, and frontend visualization
- **Week 3**: REST API implementation with authentication, CRUD operations, and DSA integration

## Project Structure
```text
.
├── README.md
├── .env.example
├── requirements.txt
├── index.html
├── docs/
│   ├── api_docs.md
│   ├── Database Design Document.pdf
│   ├── erd_diagram.pdf
│   └── json_mapping.md
├── screenshots/  
├── database/
│   └── database_setup.sql
├── examples/
│   └── json_schemas.json
├── web/
│   ├── styles.css
│   ├── chart_handler.js
│   └── assets/
│       └── architecture.png
├── data/
│   ├── raw/                          # XML input (git-ignored)
│   ├── processed/
│   │   └── dashboard.json
│   ├── db.sqlite3                    # Local DB (git-ignored)
│   └── logs/
│       ├── etl.log
│       └── dead_letter/
├── etl/
│   ├── config.py
│   ├── parse_xml.py
│   ├── clean_normalize.py
│   ├── categorize.py
│   ├── load_db.py
│   └── run.py
├── api/
│   ├── run_server.py
│   ├── config.py
│   ├── auth.py
│   └── handlers.py
├── dsa/
│   ├── xml_parser.py
│   └── search_comparison.py
├── scripts/
│   ├── run_etl.sh
│   ├── export_json.sh
│   ├── serve_frontend.sh
│   └── test_api.sh
└── tests/
    ├── test_parse_xml.py
    ├── test_clean_normalize.py
    └── test_categorize.py
```

## Features

### Database Design Components

#### Entity Relationship Diagram (ERD)

The ERD includes the following core entities:
* Transactions
* Users / Customers
* Transaction_Categories
* System_Logs

The diagram shows primary keys, foreign keys, relationship cardinality (1:1, 1:M, M:N), and at least one many-to-many relationship resolved using a junction table.

**Location:** `docs/erd_diagram.pdf`

#### SQL Database Implementation

The relational schema is implemented using MySQL with:
* CREATE TABLE statements with appropriate data types
* PRIMARY KEY and FOREIGN KEY constraints
* CHECK constraints for validation
* Indexed columns for performance
* Column comments for documentation
* Sample data (minimum five records per main table)

**Location:** `database/database_setup.sql`

#### JSON Data Modeling

JSON examples demonstrate how relational data is serialized for API responses.

**Location:** `examples/json_schemas.json`

### REST API Features

- **CRUD Operations**: Full Create, Read, Update, Delete functionality for transactions
- **Basic Authentication**: Secure endpoint protection with 401 Unauthorized responses
- **XML to JSON Parsing**: Converts SMS transaction records from XML format to JSON
- **DSA Integration**: Linear search vs. dictionary lookup implementation with performance analysis
- **Comprehensive Documentation**: Complete API endpoint specifications with examples

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd momo-sms-analytics
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` or set environment variables:
```bash
# Database Configuration
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=momo-sms-analytics
export DB_PORT=3306

# API Authentication
export API_USERNAME=admin
export API_PASSWORD=password
```

### 5. Add XML Data

Place your XML file in:
```
data/raw/modified_sms_v2.xml
```

### 6. Run ETL Pipeline (Optional)
```bash
bash scripts/run_etl.sh
```

or
```bash
python etl/run.py --xml data/raw/modified_sms_v2.xml
```

## API Usage

### Start the REST API Server
```bash
python api/run_server.py
```

The server will start on `http://localhost:8000`

### Test the API

Run all tests:
```bash
bash scripts/test_api.sh
```

Or use curl directly:
```bash
# List all transactions
curl -X GET http://localhost:8000/transactions \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)"

# Get single transaction
curl -X GET http://localhost:8000/transactions/1 \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)"

# Create new transaction
curl -X POST http://localhost:8000/transactions \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)" \
  -H "Content-Type: application/json" \
  -d '{"type":"deposit","amount":5000,"sender":"John","receiver":"Jane"}'

# Update transaction
curl -X PUT http://localhost:8000/transactions/1 \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)" \
  -H "Content-Type: application/json" \
  -d '{"amount":6000}'

# Delete transaction
curl -X DELETE http://localhost:8000/transactions/1 \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)"
```

### API Endpoints

- `GET /transactions` - List all transactions
- `GET /transactions/{id}` - Get single transaction
- `POST /transactions` - Create new transaction
- `PUT /transactions/{id}` - Update transaction
- `DELETE /transactions/{id}` - Delete transaction

See `docs/api_docs.md` for complete documentation including request/response examples and error codes.

## Data Structures & Algorithms

### Run DSA Comparison

Compare linear search vs dictionary lookup performance:
```bash
python dsa/search_comparison.py
```

This demonstrates:
- Linear search implementation for finding transactions
- Dictionary lookup implementation (O(1) access)
- Performance comparison with timing results
- Analysis of efficiency differences

### Parse XML to JSON
```bash
python dsa/xml_parser.py
```

Or use in Python:
```python
from dsa.xml_parser import parse_xml_file

transactions = parse_xml_file('data/raw/modified_sms_v2.xml')
print(f"Parsed {len(transactions)} transactions")
```

## Frontend Dashboard

### Export Dashboard JSON
```bash
bash scripts/export_json.sh
```

### Serve Frontend
```bash
bash scripts/serve_frontend.sh
```

Open in browser: `http://localhost:8000`

## Testing

### Run Unit Tests
```bash
python -m pytest tests/
```

### API Testing

Test screenshots are available in `screenshots/` directory including:
- Successful GET with authentication
- Unauthorized request (401 error)
- Successful POST, PUT, DELETE operations

## Team Collaboration and Version Control

* All team members contributed through GitHub commits
* Code commits are the only evidence of contribution
* Files are organized into required folders
* Scrum board updated with completed tasks and sprint planning

### Scrum Board

[https://github.com/users/Abdull-Kudus/projects/2](https://github.com/users/Abdull-Kudus/projects/2)

### AI Usage Log

| Date       | Tool      | Purpose                       | Used For                                                   |
| ---------- | --------- | ----------------------------- | ---------------------------------------------------------- |
| 27/01/2026 | ChatGPT   | Formatting and styling README | Helped structure and format README for GitHub presentation |
| 02/02/2026 | Claude    | API documentation             | Assisted with API endpoint documentation structure         |
| [dd/mm]    | Grammarly | Grammar                       | Documentation proofreading                                 |

All design decisions were made by team members.

## System Architecture

![System Architecture](web/assets/architecture.png)

## Documentation

- **API Documentation**: `docs/api_docs.md`
- **Database Design**: `docs/Database Design Document.pdf`
- **ERD Diagram**: `docs/erd_diagram.pdf`
- **JSON Mapping**: `docs/json_mapping.md`