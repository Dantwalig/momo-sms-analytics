"""
REST API server using Python's http.server module.
Implements Basic Authentication and CRUD operations for transactions.
"""

import json
import base64
import re
import sys
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, Optional, Tuple

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.db import get_db_connection
from api.config import AUTH_USERNAME, AUTH_PASSWORD


class TransactionAPIHandler(BaseHTTPRequestHandler):
    """Custom HTTP request handler for Transaction API."""
    
    def _set_cors_headers(self):
        """Set CORS headers for cross-origin requests."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    
    def _send_response(self, status_code: int, data: Any = None, message: str = None):
        """Send JSON response with status code."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        
        response = {}
        if data is not None:
            response['data'] = data
        if message:
            response['message'] = message
        
        if response:
            self.wfile.write(json.dumps(response, default=str).encode('utf-8'))
        else:
            self.wfile.write(b'{}')
    
    def _send_error(self, status_code: int, message: str):
        """Send error response."""
        self._send_response(status_code, message=message)
    
    def _authenticate(self) -> bool:
        """Check Basic Authentication credentials."""
        auth_header = self.headers.get('Authorization', '')
        
        if not auth_header.startswith('Basic '):
            return False
        
        try:
            # Extract and decode base64 credentials
            encoded_credentials = auth_header.split(' ')[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':', 1)
            
            # Validate credentials
            return username == AUTH_USERNAME and password == AUTH_PASSWORD
        except Exception:
            return False
    
    def _require_auth(self) -> bool:
        """Require authentication, return False if unauthorized."""
        if not self._authenticate():
            self.send_response(401)
            self.send_header('Content-Type', 'application/json')
            self.send_header('WWW-Authenticate', 'Basic realm="API"')
            self._set_cors_headers()
            self.end_headers()
            error_response = {'error': 'Unauthorized', 'message': 'Invalid credentials'}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
            return False
        return True
    
    def _parse_path(self) -> Tuple[str, Optional[str]]:
        """Parse URL path to extract endpoint and ID."""
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        if len(path_parts) == 1 and path_parts[0] == 'transactions':
            return 'transactions', None
        elif len(path_parts) == 2 and path_parts[0] == 'transactions':
            return 'transactions', path_parts[1]
        else:
            return 'unknown', None
    
    def _read_json_body(self) -> Optional[Dict[str, Any]]:
        """Read and parse JSON request body."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                return None
            
            body = self.rfile.read(content_length)
            return json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            return None
        except Exception:
            return None
    
    def _get_all_transactions(self):
        """Handle GET /transactions - List all transactions."""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT 
                        transaction_id,
                        transaction_reference,
                        amount,
                        transaction_type,
                        transaction_status,
                        transaction_date,
                        category_id,
                        raw_sms_body
                    FROM Transaction
                    ORDER BY transaction_date DESC
                """)
                transactions = cursor.fetchall()
                cursor.close()
                
                # Convert Decimal to float for JSON serialization
                for txn in transactions:
                    if txn.get('amount') is not None:
                        txn['amount'] = float(txn['amount'])
                
                self._send_response(200, transactions)
        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")
    
    def _get_transaction_by_id(self, transaction_id: str):
        """Handle GET /transactions/{id} - Get single transaction."""
        try:
            transaction_id_int = int(transaction_id)
        except ValueError:
            self._send_error(400, "Invalid transaction ID")
            return
        
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT 
                        transaction_id,
                        transaction_reference,
                        amount,
                        transaction_type,
                        transaction_status,
                        transaction_date,
                        category_id,
                        raw_sms_body
                    FROM Transaction
                    WHERE transaction_id = %s
                """, (transaction_id_int,))
                
                transaction = cursor.fetchone()
                cursor.close()
                
                if not transaction:
                    self._send_error(404, "Transaction not found")
                    return
                
                # Convert Decimal to float for JSON serialization
                if transaction.get('amount') is not None:
                    transaction['amount'] = float(transaction['amount'])
                
                self._send_response(200, transaction)
        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")
    
    def _create_transaction(self):
        """Handle POST /transactions - Create new transaction."""
        data = self._read_json_body()
        
        if not data:
            self._send_error(400, "Invalid JSON or empty body")
            return
        
        # Validate required fields
        required_fields = ['transaction_reference', 'amount', 'transaction_date']
        for field in required_fields:
            if field not in data:
                self._send_error(400, f"Missing required field: {field}")
                return
        
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Transaction 
                    (transaction_reference, amount, transaction_type, transaction_status, 
                     transaction_date, category_id, raw_sms_body)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    data.get('transaction_reference'),
                    data.get('amount'),
                    data.get('transaction_type', 'DEBIT'),
                    data.get('transaction_status', 'Completed'),
                    data.get('transaction_date'),
                    data.get('category_id'),
                    data.get('raw_sms_body', '')
                ))
                
                transaction_id = cursor.lastrowid
                conn.commit()
                cursor.close()
                
                # Fetch the created transaction
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT 
                        transaction_id,
                        transaction_reference,
                        amount,
                        transaction_type,
                        transaction_status,
                        transaction_date,
                        category_id,
                        raw_sms_body
                    FROM Transaction
                    WHERE transaction_id = %s
                """, (transaction_id,))
                
                transaction = cursor.fetchone()
                cursor.close()
                
                if transaction and transaction.get('amount') is not None:
                    transaction['amount'] = float(transaction['amount'])
                
                self._send_response(201, transaction, "Transaction created successfully")
        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")
    
    def _update_transaction(self, transaction_id: str):
        """Handle PUT /transactions/{id} - Update transaction."""
        try:
            transaction_id_int = int(transaction_id)
        except ValueError:
            self._send_error(400, "Invalid transaction ID")
            return
        
        data = self._read_json_body()
        
        if not data:
            self._send_error(400, "Invalid JSON or empty body")
            return
        
        try:
            with get_db_connection() as conn:
                # Check if transaction exists
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT transaction_id FROM Transaction WHERE transaction_id = %s", 
                             (transaction_id_int,))
                if not cursor.fetchone():
                    cursor.close()
                    self._send_error(404, "Transaction not found")
                    return
                cursor.close()
                
                # Build update query dynamically based on provided fields
                update_fields = []
                update_values = []
                
                allowed_fields = ['transaction_reference', 'amount', 'transaction_type', 
                                'transaction_status', 'transaction_date', 'category_id', 'raw_sms_body']
                
                for field in allowed_fields:
                    if field in data:
                        update_fields.append(f"{field} = %s")
                        update_values.append(data[field])
                
                if not update_fields:
                    self._send_error(400, "No valid fields to update")
                    return
                
                update_values.append(transaction_id_int)
                
                cursor = conn.cursor()
                cursor.execute(f"""
                    UPDATE Transaction 
                    SET {', '.join(update_fields)}
                    WHERE transaction_id = %s
                """, update_values)
                
                conn.commit()
                cursor.close()
                
                # Fetch updated transaction
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT 
                        transaction_id,
                        transaction_reference,
                        amount,
                        transaction_type,
                        transaction_status,
                        transaction_date,
                        category_id,
                        raw_sms_body
                    FROM Transaction
                    WHERE transaction_id = %s
                """, (transaction_id_int,))
                
                transaction = cursor.fetchone()
                cursor.close()
                
                if transaction and transaction.get('amount') is not None:
                    transaction['amount'] = float(transaction['amount'])
                
                self._send_response(200, transaction, "Transaction updated successfully")
        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")
    
    def _delete_transaction(self, transaction_id: str):
        """Handle DELETE /transactions/{id} - Delete transaction."""
        try:
            transaction_id_int = int(transaction_id)
        except ValueError:
            self._send_error(400, "Invalid transaction ID")
            return
        
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Transaction WHERE transaction_id = %s", 
                             (transaction_id_int,))
                
                if cursor.rowcount == 0:
                    cursor.close()
                    self._send_error(404, "Transaction not found")
                    return
                
                conn.commit()
                cursor.close()
                
                self.send_response(204)
                self._set_cors_headers()
                self.end_headers()
        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")
    
    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS preflight."""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        if not self._require_auth():
            return
        
        endpoint, resource_id = self._parse_path()
        
        if endpoint == 'transactions' and resource_id is None:
            self._get_all_transactions()
        elif endpoint == 'transactions' and resource_id:
            self._get_transaction_by_id(resource_id)
        else:
            self._send_error(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests."""
        if not self._require_auth():
            return
        
        endpoint, resource_id = self._parse_path()
        
        if endpoint == 'transactions' and resource_id is None:
            self._create_transaction()
        else:
            self._send_error(404, "Endpoint not found")
    
    def do_PUT(self):
        """Handle PUT requests."""
        if not self._require_auth():
            return
        
        endpoint, resource_id = self._parse_path()
        
        if endpoint == 'transactions' and resource_id:
            self._update_transaction(resource_id)
        else:
            self._send_error(404, "Endpoint not found")
    
    def do_DELETE(self):
        """Handle DELETE requests."""
        if not self._require_auth():
            return
        
        endpoint, resource_id = self._parse_path()
        
        if endpoint == 'transactions' and resource_id:
            self._delete_transaction(resource_id)
        else:
            self._send_error(404, "Endpoint not found")
    
    def log_message(self, format, *args):
        """Override to customize log format."""
        print(f"[{self.address_string()}] {format % args}")
