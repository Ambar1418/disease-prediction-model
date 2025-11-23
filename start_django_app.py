#!/usr/bin/env python3
"""
Startup script for Django app with integrated ML model
This script initializes the ML model and starts the Django development server
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path

def setup_environment():
    """Setup the environment and install dependencies"""
    print("🔧 Setting up environment...")
    
    # Add the project root to Python path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Change to the Django project directory
    django_dir = project_root / "minor"
    os.chdir(django_dir)
    # Ensure Django app imports work
    sys.path.insert(0, str(django_dir))
    
    print(f"📁 Working directory: {os.getcwd()}")
    
    # macOS-specific environment setup
    if sys.platform == "darwin":
        print("🍎 macOS detected - optimizing for Apple Silicon")
        # Set environment variables for better macOS performance
        os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')  # Reduce TensorFlow logging
        os.environ.setdefault('OMP_NUM_THREADS', '4')  # Optimize CPU usage

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import django
        import numpy
        import PIL
        print("✅ Core dependencies are installed")
        # TensorFlow and keras-related packages are optional for server startup
        try:
            import tensorflow  # noqa: F401
            print("✅ TensorFlow detected")
        except Exception:
            print("⚠️ TensorFlow not detected. The app will start, but ML predictions will be disabled until dependencies are installed.")
        return True
    except ImportError as e:
        print(f"❌ Missing core dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def initialize_ml_model():
    """Initialize the ML model in a separate thread"""
    print("🤖 Initializing ML model...")
    
    def load_model():
        try:
            # Import and initialize the ML service
            from myapp.ml_service import ml_service
            print("✅ ML model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading ML model: {e}")
    
    # Run model loading in background
    model_thread = threading.Thread(target=load_model)
    model_thread.daemon = True
    model_thread.start()
    
    # Give it a moment to load
    time.sleep(2)

def run_django_migrations():
    """Run Django migrations"""
    print("🗄️ Running Django migrations...")
    
    try:
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        print("✅ Migrations completed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    return True

def start_django_server():
    """Start the Django development server"""
    print("🚀 Starting Django development server...")
    print("📱 Access the application at: http://127.0.0.1:8000")
    print("🔮 ML prediction page: http://127.0.0.1:8000/predict")
    print("📊 Admin panel: http://127.0.0.1:8000/admin")
    print("\n" + "="*60)
    print("🎉 Django app with integrated ML model is running!")
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    try:
        subprocess.run([sys.executable, "manage.py", "runserver"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server error: {e}")

def main():
    """Main function to start the application"""
    print("🏥 Hair Disease Prediction - Django Integration")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Initialize ML model
    initialize_ml_model()
    
    # Run migrations
    if not run_django_migrations():
        sys.exit(1)
    
    # Start Django server
    start_django_server()

if __name__ == "__main__":
    main()
