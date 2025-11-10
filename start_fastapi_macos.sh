#!/bin/bash

# macOS FastAPI Startup Script
echo "🍎 Starting FastAPI server on macOS..."

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️ Virtual environment not found, using system Python"
fi

# Start FastAPI with uvicorn
echo "🚀 Starting FastAPI server with uvicorn..."
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
