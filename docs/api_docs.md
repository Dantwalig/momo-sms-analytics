# REST API Documentation

## Overview

This REST API provides secure access to SMS transaction data from the MoMo (Mobile Money) service. The API implements Basic Authentication and supports full CRUD operations on transaction records.

**Base URL**: `http://localhost:8000`

**Authentication**: Basic Authentication (default: `admin:password`)

## Authentication

All endpoints require Basic Authentication. Include the `Authorization` header with base64-encoded credentials:

```
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
```

To generate the base64 string:
```bash
echo -n "admin:password" | base64
```

## Endpoints

### 1. List All Transactions

**GET** `/transactions`

Retrieve all transactions from the database.

#### Request

```bash
curl -X GET http://localhost:8000/transactions \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQ="
```

#### Response

**Status Code**: `200 OK`

```json
{
  "data": [
    {
      "transaction_id": 1,
      "transaction_reference": "76662021700",
      "amount": 2000.0,
      "transaction_type": "CREDIT",
      "transaction_status": "Completed",
      "transaction_date": "2024-05-10 16:30:51",
      "category_id": 1,
      "raw_sms_body": "You have received 2000 RWF from Jane Smith..."
    },
    {
      "transaction_id": 2,
      "transaction_reference": "73214484437",
      "amount": 1000.0,
      "transaction_type": "DEBIT",
      "transaction_status": "Completed",
      "transaction_date": "2024-05-10 16:31:39",
      "category_id": 2,
      "raw_sms_body": "TxId: 73214484437. Your payment of 1,000 RWF..."
    }
  ]
}
```

#### Error Codes

- `401 Unauthorized`: Invalid or missing credentials
- `500 Internal Server Error`: Database or server error

---

### 2. Get Single Transaction

**GET** `/transactions/{id}`

Retrieve a specific transaction by its ID.

#### Request

```bash
curl -X GET http://localhost:8000/transactions/1 \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQ="
```

#### Response

**Status Code**: `200 OK`

```json
{
  "data": {
    "transaction_id": 1,
    "transaction_reference": "76662021700",
    "amount": 2000.0,
    "transaction_type": "CREDIT",
    "transaction_status": "Completed",
    "transaction_date": "2024-05-10 16:30:51",
    "category_id": 1,
    "raw_sms_body": "You have received 2000 RWF from Jane Smith..."
  }
}
```

#### Error Codes

- `400 Bad Request`: Invalid transaction ID format
- `401 Unauthorized`: Invalid or missing credentials
- `404 Not Found`: Transaction with specified ID does not exist
- `500 Internal Server Error`: Database or server error

---

### 3. Create Transaction

**POST** `/transactions`

Create a new transaction record.

#### Request

```bash
curl -X POST http://localhost:8000/transactions \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQ=" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_reference": "TXN123456789",
    "amount": 5000.00,
    "transaction_type": "DEBIT",
    "transaction_status": "Completed",
    "transaction_date": "2024-05-20 10:30:00",
    "category_id": 1,
    "raw_sms_body": "Transaction details here..."
  }'
```

#### Request Body Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `transaction_reference` | string | Yes | Unique transaction reference code |
| `amount` | decimal | Yes | Transaction amount |
| `transaction_type` | string | No | Type: DEBIT, CREDIT (default: DEBIT) |
| `transaction_status` | string | No | Status: Completed, Pending, Failed (default: Completed) |
| `transaction_date` | datetime | Yes | Transaction date and time |
| `category_id` | integer | No | Category ID (foreign key) |
| `raw_sms_body` | string | No | Original SMS content |

#### Response

**Status Code**: `201 Created`

```json
{
  "data": {
    "transaction_id": 100,
    "transaction_reference": "TXN123456789",
    "amount": 5000.0,
    "transaction_type": "DEBIT",
    "transaction_status": "Completed",
    "transaction_date": "2024-05-20 10:30:00",
    "category_id": 1,
    "raw_sms_body": "Transaction details here..."
  },
  "message": "Transaction created successfully"
}
```

#### Error Codes

- `400 Bad Request`: Invalid JSON, missing required fields, or invalid data format
- `401 Unauthorized`: Invalid or missing credentials
- `500 Internal Server Error`: Database or server error

---

### 4. Update Transaction

**PUT** `/transactions/{id}`

Update an existing transaction record.

#### Request

```bash
curl -X PUT http://localhost:8000/transactions/1 \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQ=" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 3000.00,
    "transaction_status": "Pending"
  }'
```

#### Request Body Fields

All fields are optional. Only include fields you want to update.

| Field | Type | Description |
|-------|------|-------------|
| `transaction_reference` | string | Unique transaction reference code |
| `amount` | decimal | Transaction amount |
| `transaction_type` | string | Type: DEBIT, CREDIT |
| `transaction_status` | string | Status: Completed, Pending, Failed |
| `transaction_date` | datetime | Transaction date and time |
| `category_id` | integer | Category ID (foreign key) |
| `raw_sms_body` | string | Original SMS content |

#### Response

**Status Code**: `200 OK`

```json
{
  "data": {
    "transaction_id": 1,
    "transaction_reference": "76662021700",
    "amount": 3000.0,
    "transaction_type": "CREDIT",
    "transaction_status": "Pending",
    "transaction_date": "2024-05-10 16:30:51",
    "category_id": 1,
    "raw_sms_body": "You have received 2000 RWF from Jane Smith..."
  },
  "message": "Transaction updated successfully"
}
```

#### Error Codes

- `400 Bad Request`: Invalid transaction ID format, invalid JSON, or no valid fields to update
- `401 Unauthorized`: Invalid or missing credentials
- `404 Not Found`: Transaction with specified ID does not exist
- `500 Internal Server Error`: Database or server error

---

### 5. Delete Transaction

**DELETE** `/transactions/{id}`

Delete a transaction record.

#### Request

```bash
curl -X DELETE http://localhost:8000/transactions/1 \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQ="
```

#### Response

**Status Code**: `204 No Content`

No response body.

#### Error Codes

- `400 Bad Request`: Invalid transaction ID format
- `401 Unauthorized`: Invalid or missing credentials
- `404 Not Found`: Transaction with specified ID does not exist
- `500 Internal Server Error`: Database or server error

---

## Error Response Format

All error responses follow this format:

```json
{
  "error": "Error Type",
  "message": "Detailed error message"
}
```

Example (401 Unauthorized):

```json
{
  "error": "Unauthorized",
  "message": "Invalid credentials"
}
```

## HTTP Status Codes

| Code | Description |
|------|-------------|
| `200` | OK - Request successful |
| `201` | Created - Resource created successfully |
| `204` | No Content - Resource deleted successfully |
| `400` | Bad Request - Invalid request data or format |
| `401` | Unauthorized - Authentication required or invalid credentials |
| `404` | Not Found - Resource not found |
| `500` | Internal Server Error - Server or database error |

## CORS Support

The API includes CORS headers to allow cross-origin requests:

- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Authorization`

## Security Notes

### Basic Authentication Limitations

Basic Authentication is simple but has security limitations:

1. **Credentials in Every Request**: Username and password are sent with every request, increasing exposure risk
2. **Base64 Encoding Only**: Credentials are base64-encoded, not encrypted. They can be easily decoded if intercepted
3. **No Token Expiration**: Credentials don't expire, so compromised credentials remain valid until changed
4. **No Refresh Mechanism**: No way to refresh credentials without re-authenticating

### Recommended Alternatives

For production use, consider:

1. **JWT (JSON Web Tokens)**: 
   - Stateless authentication with token expiration
   - Tokens can be refreshed without re-entering credentials
   - More secure than Basic Auth

2. **OAuth 2.0**:
   - Industry-standard authorization framework
   - Supports token refresh and revocation
   - Better suited for third-party integrations

3. **API Keys**:
   - Simple alternative with better security than Basic Auth
   - Can be rotated and revoked easily

## Testing

See `scripts/test_api.sh` for comprehensive testing examples using curl.

## Database Schema

Transactions are stored in the `Transaction` table with the following structure:

- `transaction_id` (INT, Primary Key)
- `transaction_reference` (VARCHAR, Unique)
- `amount` (DECIMAL)
- `transaction_type` (VARCHAR)
- `transaction_status` (VARCHAR)
- `transaction_date` (DATETIME)
- `category_id` (INT, Foreign Key)
- `raw_sms_body` (TEXT)
