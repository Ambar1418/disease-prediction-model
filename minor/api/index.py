"""
Vercel serverless function entry point for Django
"""
import os
import sys
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ.setdefault('VERCEL', '1')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Vercel's @vercel/python builder expects 'app' or 'application'
application = get_wsgi_application()
app = application

