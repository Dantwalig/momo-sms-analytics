"""
Server entry point for REST API.
Starts HTTP server on configured port.
"""

import signal
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from http.server import HTTPServer
from api.server import TransactionAPIHandler
from api.config import SERVER_HOST, SERVER_PORT, AUTH_USERNAME, AUTH_PASSWORD


def signal_handler(sig, frame):
    """Handle graceful shutdown on SIGINT or SIGTERM."""
    print('\nShutting down server...')
    sys.exit(0)


def main():
    """Start the HTTP server."""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create server instance
    server_address = (SERVER_HOST, SERVER_PORT)
    httpd = HTTPServer(server_address, TransactionAPIHandler)
    
    print(f"Starting REST API server on http://{SERVER_HOST}:{SERVER_PORT}")
    print(f"Basic Auth credentials: {AUTH_USERNAME}:{AUTH_PASSWORD}")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Start server
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    finally:
        httpd.server_close()
        print("Server closed")


if __name__ == '__main__':
    main()
