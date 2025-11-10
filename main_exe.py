#!/usr/bin/env python3
"""
Main executable entry point for Hair Disease Prediction App
This script initializes Django and starts the web server
"""

import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Add the bundled Django app to Python path
if hasattr(sys, '_MEIPASS'):
    # Running as PyInstaller bundle
    bundle_dir = Path(sys._MEIPASS)
    django_dir = bundle_dir / "minor"
else:
    # Running as script
    bundle_dir = Path(__file__).parent
    django_dir = bundle_dir / "minor"

sys.path.insert(0, str(bundle_dir))
sys.path.insert(0, str(django_dir))

# Change to Django directory
os.chdir(django_dir)

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minor.settings')
    
    try:
        # Import TensorFlow first to ensure it's available
        print("🤖 Loading TensorFlow...")
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__} loaded successfully")
        
        # Import Django
        print("🌐 Loading Django...")
        import django
        django.setup()
        print("✅ Django initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        print("💡 This might be due to missing dependencies in the executable")
        return False

def run_migrations():
    """Run Django migrations"""
    print("🗄️ Running database migrations...")
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        print("✅ Database migrations completed")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def start_server():
    """Start Django development server"""
    print("🚀 Starting Hair Disease Prediction Server...")
    print("=" * 60)
    print("🏥 Hair Disease Prediction Application")
    print("=" * 60)
    print("📱 Application will be available at: http://127.0.0.1:8000")
    print("🔮 ML Prediction: http://127.0.0.1:8000/predict")
    print("📊 Admin Panel: http://127.0.0.1:8000/admin")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Auto-open browser after a short delay
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open('http://127.0.0.1:8000')
        except:
            pass
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        print("💡 Trying alternative server start method...")
        try:
            import subprocess
            subprocess.run(['python', 'manage.py', 'runserver', '127.0.0.1:8000'], check=True)
        except Exception as e2:
            print(f"❌ Alternative method also failed: {e2}")

def main():
    """Main function"""
    print("🏥 Hair Disease Prediction - Executable Version")
    print("=" * 50)
    
    # Setup Django
    if not setup_django():
        input("Press Enter to exit...")
        return
    
    # Run migrations
    if not run_migrations():
        input("Press Enter to exit...")
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
