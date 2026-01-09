#!/bin/bash
# Serve frontend using Python's HTTP server

PORT="${1:-8000}"

echo "Starting frontend server on http://localhost:$PORT"
echo "Open http://localhost:$PORT in your browser"

# Serve from project root
python3 -m http.server "$PORT"

