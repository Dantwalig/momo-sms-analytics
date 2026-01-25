# SQL to JSON Mapping

## Overview

This document shows how our SQL database tables are converted to JSON format.

---

## 1. User Entity

### SQL Table: User

```sql
CREATE TABLE User (
    user_id INT PRIMARY KEY,
    phone_number VARCHAR(15),
    contact_name VARCHAR(100),
    user_type VARCHAR(20),
    created_at DATETIME
);
```

**JSON Representation:**

```json
{
  "user_id": 1,
  "phone_number": "250791666666",
  "contact_name": "Jane Smith",
  "user_type": "individual",
  "created_at": "2024-05-10T16:30:51Z"
}
```

**Mapping:**

- user_id (INT) → user_id (number)
- phone_number (VARCHAR) → phone_number (string)
- contact_name (VARCHAR) → contact_name (string)
- user_type (VARCHAR) → user_type (string)
- created_at (DATETIME) → created_at (string in ISO 8601 format)

---

## 2. Category Entity

## SQL Table: Category

```sql
CREATE TABLE Category (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(50),
    description VARCHAR(255),
    created_at DATETIME
);
```

**JSON Representation:**

```json
{
  "category_id": 1,
  "category_name": "transfer",
  "description": "Person-to-person money transfer",
  "created_at": "2024-05-10T00:00:00Z"
}
```

**Mapping:**

- category_id (INT) → category_id (number)
- category_name (VARCHAR) → category_name (string)
- description (VARCHAR) → description (string)
- created_at (DATETIME) → created_at (string)

---

## 3. Transaction Entity

## SQL Table: Transaction

```sql
CREATE TABLE Transaction (
    transaction_id INT PRIMARY KEY,
    transaction_reference VARCHAR(50),
    amount DECIMAL(15,2),
    transaction_type VARCHAR(20),
    transaction_status VARCHAR(20),
    transaction_date DATETIME,
    category_id INT,
    raw_sms_body TEXT,
    balance_after DECIMAL(15,2),
    FOREIGN KEY (category_id) REFERENCES Category(category_id)
);
```

**JSON Representation:**

```json
{
  "transaction_id": 1,
  "transaction_reference": "76662021700",
  "amount": 2000.00,
  "transaction_type": "received",
  "transaction_status": "completed",
  "transaction_date": "2024-05-10T16:30:51Z",
  "category_id": 1,
  "raw_sms_body": "You have received 2000 RWF from Jane Smith...",
  "balance_after": 2000.00
}
```

**Mapping:**

- transaction_id (INT) → transaction_id (number)
- transaction_reference (VARCHAR) → transaction_reference (string)
- amount (DECIMAL) → amount (number)
- transaction_type (VARCHAR) → transaction_type (string)
- transaction_status (VARCHAR) → transaction_status (string)
- transaction_date (DATETIME) → transaction_date (string)
- category_id (INT) → category_id (number)
- raw_sms_body (TEXT) → raw_sms_body (string)
- balance_after (DECIMAL) → balance_after (number)

---

## 4. Role Entity

## SQL Table: Role

```sql
CREATE TABLE Role (
    role_id INT PRIMARY KEY,
    user_id INT,
    transaction_id INT,
    role_type VARCHAR(20),
    assigned_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (transaction_id) REFERENCES Transaction(transaction_id)
);
```

**JSON Representation:**

```json
{
  "role_id": 1,
  "user_id": 2,
  "transaction_id": 1,
  "role_type": "sender",
  "assigned_at": "2024-05-10T16:30:51Z"
}
```

**Mapping:**

- role_id (INT) → role_id (number)
- user_id (INT) → user_id (number)
- transaction_id (INT) → transaction_id (number)
- role_type (VARCHAR) → role_type (string)
- assigned_at (DATETIME) → assigned_at (string)

---

## 5. System_Log Entity

## SQL Table: System_Log

```sql
CREATE TABLE System_Log (
    log_id INT PRIMARY KEY,
    transaction_id INT,
    log_status VARCHAR(20),
    service_center VARCHAR(20),
    readable_date VARCHAR(50),
    logged_at DATETIME,
    FOREIGN KEY (transaction_id) REFERENCES Transaction(transaction_id)
);
```

**JSON Representation:**

```json
{
  "log_id": 1,
  "transaction_id": 1,
  "log_status": "success",
  "service_center": "+250788110381",
  "readable_date": "10 May 2024 4:30:58 PM",
  "logged_at": "2024-05-10T16:30:58Z"
}
```

**Mapping:**

- log_id (INT) → log_id (number)
- transaction_id (INT) → transaction_id (number)
- log_status (VARCHAR) → log_status (string)
- service_center (VARCHAR) → service_center (string)
- readable_date (VARCHAR) → readable_date (string)
- logged_at (DATETIME) → logged_at (string)

---

## Complex Nested JSON (Sophisticated Nesting)

## Complete Transaction with All Related Data

This shows how multiple SQL tables are combined into one nested JSON object.

**SQL Query:**

```sql
SELECT t.*, c.*, r.role_type, u.*, sl.*
FROM Transaction t
LEFT JOIN Category c ON t.category_id = c.category_id
LEFT JOIN Role r ON t.transaction_id = r.transaction_id
LEFT JOIN User u ON r.user_id = u.user_id
LEFT JOIN System_Log sl ON t.transaction_id = sl.transaction_id
WHERE t.transaction_id = 1;
```

**JSON Output:**

```json
{
  "transaction_id": 1,
  "transaction_reference": "76662021700",
  "amount": 2000.00,
  "transaction_type": "received",
  "transaction_status": "completed",
  "transaction_date": "2024-05-10T16:30:51Z",
  "balance_after": 2000.00,
  "raw_sms_body": "You have received 2000 RWF from Jane Smith...",
  "category": {
    "category_id": 1,
    "category_name": "transfer",
    "description": "Person-to-person money transfer"
  },
  "participants": [
    {
      "role_type": "sender",
      "user": {
        "user_id": 2,
        "phone_number": "250788110013",
        "contact_name": "Jane Smith"
      }
    },
    {
      "role_type": "receiver",
      "user": {
        "user_id": 1,
        "phone_number": "250795963036",
        "contact_name": "Account Holder"
      }
    }
  ],
  "system_log": {
    "log_id": 1,
    "log_status": "success",
    "service_center": "+250788110381",
    "logged_at": "2024-05-10T16:30:58Z"
  }
}
```

**How Nesting Works:**

1. **Foreign Key Becomes Nested Object**
   - SQL: `category_id = 1` (foreign key)
   - JSON: `"category": { "category_id": 1, "category_name": "transfer", ... }`

2. **Junction Table Becomes Array**
   - SQL: Role table with multiple rows
   - JSON: `"participants": [ {...}, {...} ]`

3. **Related Table Becomes Nested Object**
   - SQL: System_Log table
   - JSON: `"system_log": { "log_id": 1, ... }`

---

## Data Type Conversion Summary

| SQL Type | JSON Type | Example |
| ---------- | ----------- | --------- |
| INT | number | `123` |
| DECIMAL | number | `2000.00` |
| VARCHAR | string | `"Jane Smith"` |
| TEXT | string | `"Long text..."` |
| DATETIME | string | `"2024-05-10T16:30:51Z"` |

**Note:** DATETIME is converted to ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) in JSON.

---
Understanding Serialization
Serialization means converting database data (SQL) into JSON format for:

API responses
Data export
Frontend communication

Key Principles:

Flat SQL tables become nested JSON objects when relationships exist
DATETIME fields convert to ISO 8601 strings for universal compatibility
Foreign keys become embedded objects to reduce API calls
Junction tables become arrays to represent many-to-many relationships

This mapping allows our MoMo SMS analytics system to efficiently serve data to web applications while maintaining the structured relationships defined in our database.
