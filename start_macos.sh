#!/bin/bash

# macOS Startup Script for Hair Disease Prediction
echo "🍎 Starting Hair Disease Prediction on macOS..."

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️ Virtual environment not found, using system Python"
fi

# Start the Django application
echo "🚀 Starting Django application..."
python3 start_django_app.py
