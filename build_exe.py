#!/usr/bin/env python3
"""
Build script to create executable from Django disease prediction app
This script uses PyInstaller to bundle the Django application with all dependencies
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    print("🔧 Installing PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install PyInstaller: {e}")
        return False

def create_main_executable():
    """Create the main executable entry point"""
    main_content = '''#!/usr/bin/env python3
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
        import django
        django.setup()
        print("✅ Django initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Django initialization failed: {e}")
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
        print("\\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

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
'''
    
    with open("main_exe.py", "w", encoding="utf-8") as f:
        f.write(main_content)
    print("✅ Created main executable script")

def create_pyinstaller_spec():
    """Create PyInstaller spec file"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# Get the current directory
current_dir = Path.cwd()

# Define paths
django_dir = current_dir / "minor"
model_file = current_dir / "hair-diseases.h5"

# Collect all Django files
django_files = []
for root, dirs, files in os.walk(django_dir):
    for file in files:
        if file.endswith(('.py', '.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico')):
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, current_dir)
            django_files.append((src_path, os.path.dirname(rel_path)))

# Collect model file
model_files = []
if model_file.exists():
    model_files.append((str(model_file), '.'))

# Collect frontend files
frontend_files = []
frontend_dir = current_dir / "frontend"
if frontend_dir.exists():
    for root, dirs, files in os.walk(frontend_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, current_dir)
            frontend_files.append((src_path, os.path.dirname(rel_path)))

block_cipher = None

a = Analysis(
    ['main_exe.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=django_files + model_files + frontend_files,
    hiddenimports=[
        'django',
        'django.core',
        'django.core.management',
        'django.core.management.commands',
        'django.core.management.commands.runserver',
        'django.core.management.commands.migrate',
        'django.db',
        'django.db.models',
        'django.contrib',
        'django.contrib.auth',
        'django.contrib.auth.models',
        'django.contrib.auth.forms',
        'django.contrib.admin',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django.contrib.sessions.backends.db',
        'django.contrib.auth.backends',
        'django.contrib.auth.backends.ModelBackend',
        'django.contrib.sessions.models',
        'django.contrib.contenttypes.models',
        'django.contrib.sites.models',
        'django.contrib.admin.apps',
        'django.contrib.auth.apps',
        'django.contrib.contenttypes.apps',
        'django.contrib.sessions.apps',
        'django.contrib.sites.apps',
        'django.contrib.staticfiles.apps',
        'django.contrib.messages.apps',
        'django.contrib.messages.storage',
        'django.contrib.messages.storage.fallback',
        'django.contrib.messages.storage.session',
        'django.contrib.messages.storage.cookie',
        'django.contrib.messages.context_processors',
        'django.contrib.messages.middleware',
        'django.contrib.messages.utils',
        'django.contrib.messages.constants',
        'django.contrib.messages.api',
        'django.contrib.messages.models',
        'django.contrib.messages.views',
        'django.contrib.messages.forms',
        'django.contrib.messages.templatetags',
        'django.contrib.messages.templatetags.messages',
        'django.contrib.messages.templatetags.messages_extras',
        'django.contrib.messages.templatetags.messages_extras.messages',
        'django.contrib.messages.templatetags.messages_extras.messages_extras',
        'django.contrib.messages.templatetags.messages_extras.messages_extras_extras',
        'tensorflow',
        'tensorflow.keras',
        'tensorflow.keras.models',
        'tensorflow.keras.layers',
        'tensorflow.keras.utils',
        'tensorflow.keras.applications',
        'tensorflow.keras.preprocessing',
        'tensorflow.keras.preprocessing.image',
        'tensorflow.keras.backend',
        'tensorflow.keras.optimizers',
        'tensorflow.keras.losses',
        'tensorflow.keras.metrics',
        'tensorflow.keras.callbacks',
        'tensorflow.keras.initializers',
        'tensorflow.keras.regularizers',
        'tensorflow.keras.constraints',
        'tensorflow.keras.activations',
        'tensorflow.keras.utils.generic_utils',
        'tensorflow.keras.utils.data_utils',
        'tensorflow.keras.utils.io_utils',
        'tensorflow.keras.utils.layer_utils',
        'tensorflow.keras.utils.model_utils',
        'tensorflow.keras.utils.np_utils',
        'tensorflow.keras.utils.tf_utils',
        'tensorflow.keras.utils.vis_utils',
        'tensorflow.keras.utils.conv_utils',
        'tensorflow.keras.utils.generic_utils',
        'tensorflow.keras.utils.data_utils',
        'tensorflow.keras.utils.io_utils',
        'tensorflow.keras.utils.layer_utils',
        'tensorflow.keras.utils.model_utils',
        'tensorflow.keras.utils.np_utils',
        'tensorflow.keras.utils.tf_utils',
        'tensorflow.keras.utils.vis_utils',
        'tensorflow.keras.utils.conv_utils',
        'keras_self_attention',
        'keras_multi_head',
        'PIL',
        'PIL.Image',
        'numpy',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'visualkeras',
        'myapp',
        'myapp.models',
        'myapp.views',
        'myapp.ml_service',
        'myapp.apps',
        'myapp.admin',
        'myapp.tests',
        'myapp.middleware',
        'minor',
        'minor.settings',
        'minor.urls',
        'minor.wsgi',
        'minor.asgi',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HairDiseasePrediction',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open("HairDiseasePrediction.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    print("✅ Created PyInstaller spec file")

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...")
    try:
        # Clean previous builds
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("dist"):
            shutil.rmtree("dist")
        
        # Run PyInstaller
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "HairDiseasePrediction.spec"]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Executable built successfully!")
        print(f"📁 Executable location: {os.path.abspath('dist/HairDiseasePrediction.exe')}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_readme():
    """Create README for the executable"""
    readme_content = '''# Hair Disease Prediction - Executable Version

## Overview
This is a standalone executable version of the Hair Disease Prediction application. The executable bundles the Django web application with the machine learning model for hair disease classification.

## Features
- **10 Hair Disease Classifications**: Alopecia Areata, Contact Dermatitis, Folliculitis, Head Lice, Lichen Planus, Male Pattern Baldness, Psoriasis, Seborrheic Dermatitis, Telogen Effluvium, Tinea Capitis
- **Web Interface**: User-friendly Django web application
- **User Authentication**: Login/registration system
- **ML Prediction**: Upload images for disease classification
- **Standalone**: No need to install Python or dependencies

## How to Use

### Running the Application
1. Double-click `HairDiseasePrediction.exe`
2. The application will automatically:
   - Initialize the database
   - Start the web server
   - Open your default browser
3. If the browser doesn't open automatically, navigate to: http://127.0.0.1:8000

### Using the Application
1. **Register/Login**: Create an account or login to access the prediction feature
2. **Upload Image**: Go to the prediction page and upload a hair/scalp image
3. **Get Results**: The system will classify the image and show the predicted disease with confidence score

### System Requirements
- Windows 10/11 (64-bit)
- At least 4GB RAM
- 2GB free disk space
- Internet connection (for initial setup)

### Troubleshooting
- **Port Already in Use**: If port 8000 is busy, restart the application
- **Database Issues**: Delete `db.sqlite3` file and restart the application
- **Model Loading Issues**: Ensure the executable has write permissions in its directory

### File Structure
```
HairDiseasePrediction.exe    # Main executable
db.sqlite3                   # Database file (created automatically)
```

### Support
For issues or questions, please check the application logs in the console window.

## Technical Details
- **Framework**: Django 5.2.5
- **ML Framework**: TensorFlow 2.20.0
- **Model**: Custom CNN with attention mechanisms
- **Database**: SQLite (embedded)
- **Web Server**: Django development server
'''
    
    with open("README_EXECUTABLE.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✅ Created executable README")

def main():
    """Main build function"""
    print("🏥 Hair Disease Prediction - Executable Builder")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("minor") or not os.path.exists("hair-diseases.h5"):
        print("❌ Please run this script from the project root directory")
        print("   Expected files: minor/ directory and hair-diseases.h5")
        return False
    
    # Install PyInstaller
    if not install_pyinstaller():
        return False
    
    # Create main executable script
    create_main_executable()
    
    # Create PyInstaller spec file
    create_pyinstaller_spec()
    
    # Build executable
    if not build_executable():
        return False
    
    # Create README
    create_readme()
    
    print("=" * 60)
    print("🎉 Executable build completed successfully!")
    print(f"📁 Executable: {os.path.abspath('dist/HairDiseasePrediction.exe')}")
    print("📖 Documentation: README_EXECUTABLE.md")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        input("Press Enter to exit...")
        sys.exit(1)
