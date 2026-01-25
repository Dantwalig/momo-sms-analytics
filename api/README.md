# REST API Setup and Usage

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database Connection

Edit `api/config.py` or set environment variables:

```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=momo-sms-analytics
export DB_PORT=3306
```

### 3. Configure Authentication

Default credentials are `admin:password`. To change:

Edit `api/config.py` or set environment variables:

```bash
export API_USERNAME=your_username
export API_PASSWORD=your_password
```

### 4. Start the Server

```bash
python api/run_server.py
```

The server will start on `http://localhost:8000`

### 5. Test the API

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
```

## API Endpoints

- `GET /transactions` - List all transactions
- `GET /transactions/{id}` - Get single transaction
- `POST /transactions` - Create new transaction
- `PUT /transactions/{id}` - Update transaction
- `DELETE /transactions/{id}` - Delete transaction

See `docs/api_docs.md` for complete documentation.

## DSA Comparison

Run the data structures comparison:

```bash
python dsa/search_comparison.py
```

This will compare linear search vs dictionary lookup performance.

## XML Parsing

Parse the XML file to JSON:

```bash
python dsa/xml_parser.py
```

Or use in Python:

```python
from dsa.xml_parser import parse_xml_file

transactions = parse_xml_file('modified_sms_v2.xml')
print(f"Parsed {len(transactions)} transactions")
```
