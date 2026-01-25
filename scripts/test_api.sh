#!/bin/bash

# API Testing Script
# Tests all CRUD endpoints with curl commands

# Configuration
BASE_URL="http://localhost:8000"
USERNAME="admin"
PASSWORD="password"

# Generate base64 encoded credentials
AUTH_STRING=$(echo -n "${USERNAME}:${PASSWORD}" | base64)
AUTH_HEADER="Authorization: Basic ${AUTH_STRING}"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "REST API Testing Script"
echo "=========================================="
echo "Base URL: ${BASE_URL}"
echo "Credentials: ${USERNAME}:${PASSWORD}"
echo ""

# Test 1: GET /transactions (List all)
echo -e "${YELLOW}Test 1: GET /transactions (List all transactions)${NC}"
echo "Command: curl -X GET ${BASE_URL}/transactions -H \"${AUTH_HEADER}\""
echo ""
curl -X GET "${BASE_URL}/transactions" \
  -H "${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.' 2>/dev/null || curl -X GET "${BASE_URL}/transactions" \
  -H "${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n"
echo ""
echo "----------------------------------------"
echo ""

# Test 2: GET /transactions/{id} (Get single transaction)
echo -e "${YELLOW}Test 2: GET /transactions/1 (Get transaction by ID)${NC}"
echo "Command: curl -X GET ${BASE_URL}/transactions/1 -H \"${AUTH_HEADER}\""
echo ""
curl -X GET "${BASE_URL}/transactions/1" \
  -H "${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.' 2>/dev/null || curl -X GET "${BASE_URL}/transactions/1" \
  -H "${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n"
echo ""
echo "----------------------------------------"
echo ""

# Test 3: POST /transactions (Create new transaction)
echo -e "${YELLOW}Test 3: POST /transactions (Create new transaction)${NC}"
echo "Command: curl -X POST ${BASE_URL}/transactions -H \"${AUTH_HEADER}\" -d '{...}'"
echo ""
curl -X POST "${BASE_URL}/transactions" \
  -H "${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_reference": "TEST_TXN_001",
    "amount": 5000.00,
    "transaction_type": "DEBIT",
    "transaction_status": "Completed",
    "transaction_date": "2024-05-20 10:30:00",
    "category_id": 1,
    "raw_sms_body": "Test transaction created via API"
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.' 2>/dev/null || curl -X POST "${BASE_URL}/transactions" \
  -H "${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_reference": "TEST_TXN_001",
    "amount": 5000.00,
    "transaction_type": "DEBIT",
    "transaction_status": "Completed",
    "transaction_date": "2024-05-20 10:30:00",
    "category_id": 1,
    "raw_sms_body": "Test transaction created via API"
  }' \
  -w "\nHTTP Status: %{http_code}\n"
echo ""
echo "----------------------------------------"
echo ""

# Test 4: PUT /transactions/{id} (Update transaction)
echo -e "${YELLOW}Test 4: PUT /transactions/1 (Update transaction)${NC}"
echo "Command: curl -X PUT ${BASE_URL}/transactions/1 -H \"${AUTH_HEADER}\" -d '{...}'"
echo ""
curl -X PUT "${BASE_URL}/transactions/1" \
  -H "${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 3000.00,
    "transaction_status": "Pending"
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.' 2>/dev/null || curl -X PUT "${BASE_URL}/transactions/1" \
  -H "${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 3000.00,
    "transaction_status": "Pending"
  }' \
  -w "\nHTTP Status: %{http_code}\n"
echo ""
echo "----------------------------------------"
echo ""

# Test 5: DELETE /transactions/{id} (Delete transaction)
echo -e "${YELLOW}Test 5: DELETE /transactions/{id} (Delete transaction)${NC}"
echo "Note: This will delete a transaction. Use a test transaction ID."
echo "Command: curl -X DELETE ${BASE_URL}/transactions/{id} -H \"${AUTH_HEADER}\""
echo ""
echo "Skipping actual delete to preserve data. Uncomment below to test:"
echo "# curl -X DELETE \"${BASE_URL}/transactions/999\" \\"
echo "#   -H \"${AUTH_HEADER}\" \\"
echo "#   -w \"\\nHTTP Status: %{http_code}\\n\""
echo ""
echo "----------------------------------------"
echo ""

# Test 6: Unauthorized request (wrong credentials)
echo -e "${YELLOW}Test 6: GET /transactions (Unauthorized - wrong credentials)${NC}"
echo "Command: curl -X GET ${BASE_URL}/transactions -H \"Authorization: Basic d3Jvbmc6Y3JlZGVudGlhbHM=\""
echo ""
WRONG_AUTH="Authorization: Basic $(echo -n "wrong:credentials" | base64)"
curl -X GET "${BASE_URL}/transactions" \
  -H "${WRONG_AUTH}" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.' 2>/dev/null || curl -X GET "${BASE_URL}/transactions" \
  -H "${WRONG_AUTH}" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n"
echo ""
echo "----------------------------------------"
echo ""

# Test 7: Unauthorized request (no credentials)
echo -e "${YELLOW}Test 7: GET /transactions (Unauthorized - no credentials)${NC}"
echo "Command: curl -X GET ${BASE_URL}/transactions"
echo ""
curl -X GET "${BASE_URL}/transactions" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.' 2>/dev/null || curl -X GET "${BASE_URL}/transactions" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n"
echo ""
echo "----------------------------------------"
echo ""

# Test 8: Invalid endpoint
echo -e "${YELLOW}Test 8: GET /invalid (404 Not Found)${NC}"
echo "Command: curl -X GET ${BASE_URL}/invalid -H \"${AUTH_HEADER}\""
echo ""
curl -X GET "${BASE_URL}/invalid" \
  -H "${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.' 2>/dev/null || curl -X GET "${BASE_URL}/invalid" \
  -H "${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n"
echo ""
echo "=========================================="
echo "Testing Complete"
echo "=========================================="
echo ""
echo "For Postman testing, use these settings:"
echo "  - Method: GET/POST/PUT/DELETE"
echo "  - URL: ${BASE_URL}/transactions"
echo "  - Authorization: Basic Auth"
echo "    Username: ${USERNAME}"
echo "    Password: ${PASSWORD}"
echo ""
