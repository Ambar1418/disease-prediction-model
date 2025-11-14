#!/bin/bash
set -e

# Create required directories
echo "Creating required directories..."
mkdir -p required_files/staticfiles

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r required_files/requirements_production.txt

# Set up environment variables
export DJANGO_SETTINGS_MODULE=minor.settings
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Collect static files
echo "Collecting static files..."
python required_files/manage.py collectstatic --noinput

echo "Build completed successfully!"
