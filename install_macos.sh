#!/bin/bash

# macOS Installation Script for Hair Disease Prediction Model
# This script sets up the environment and installs macOS-specific dependencies

set -e  # Exit on any error

echo "🍎 Hair Disease Prediction - macOS Installation"
echo "================================================"

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is designed for macOS only"
    echo "   Detected OS: $OSTYPE"
    exit 1
fi

# Check Python version
echo "🐍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "   Please install Python 3.8+ from https://python.org or using Homebrew:"
    echo "   brew install python@3.11"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PYTHON_VERSION detected"

# Check if Python version is compatible
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    echo "❌ Python 3.8+ is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
VENV_DIR=".venv"
if [ -d "$VENV_DIR" ]; then
    echo "⚠️ Virtual environment already exists. Removing old one..."
    rm -rf "$VENV_DIR"
fi

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "✅ Virtual environment created and activated"

# Upgrade pip and essential tools
echo "⬆️ Upgrading pip and build tools..."
python -m pip install --upgrade pip setuptools wheel

# Install macOS-specific dependencies
echo "📚 Installing macOS-specific dependencies..."
if [ -f "requirements-macos.txt" ]; then
    echo "   Using requirements-macos.txt..."
    pip install -r requirements-macos.txt
else
    echo "   requirements-macos.txt not found, using requirements.txt..."
    pip install -r requirements.txt
fi

# Verify TensorFlow installation
echo "🔍 Verifying TensorFlow installation..."
python -c "
try:
    import tensorflow as tf
    print(f'✅ TensorFlow {tf.__version__} installed successfully')
    
    # Check for Metal support
    if hasattr(tf.config, 'list_physical_devices'):
        devices = tf.config.list_physical_devices()
        gpu_devices = [d for d in devices if 'GPU' in d.name or 'Metal' in d.name]
        if gpu_devices:
            print(f'✅ Metal GPU acceleration available: {len(gpu_devices)} device(s)')
        else:
            print('⚠️ Metal GPU acceleration not detected (CPU-only mode)')
    else:
        print('⚠️ Could not check GPU devices')
        
except ImportError as e:
    print(f'❌ TensorFlow installation failed: {e}')
    print('   The app will run but ML predictions will be disabled')
except Exception as e:
    print(f'⚠️ TensorFlow verification warning: {e}')
"

# Verify other critical dependencies
echo "🔍 Verifying other dependencies..."
python -c "
import sys
missing = []

try:
    import django
    print(f'✅ Django {django.get_version()} installed')
except ImportError:
    missing.append('django')

try:
    import PIL
    print(f'✅ Pillow {PIL.__version__} installed')
except ImportError:
    missing.append('pillow')

try:
    import numpy
    print(f'✅ NumPy {numpy.__version__} installed')
except ImportError:
    missing.append('numpy')

try:
    import fastapi
    print(f'✅ FastAPI {fastapi.__version__} installed')
except ImportError:
    missing.append('fastapi')

try:
    import uvicorn
    print(f'✅ Uvicorn {uvicorn.__version__} installed')
except ImportError:
    missing.append('uvicorn')

if missing:
    print(f'❌ Missing dependencies: {missing}')
    sys.exit(1)
else:
    print('✅ All critical dependencies verified')
"

# Check if model file exists
echo "🤖 Checking ML model..."
if [ -f "hair-diseases.h5" ]; then
    echo "✅ ML model file found: hair-diseases.h5"
else
    echo "⚠️ ML model file 'hair-diseases.h5' not found"
    echo "   The app will start but ML predictions will be disabled"
fi

# Create startup script
echo "📝 Creating macOS startup script..."
cat > start_macos.sh << 'EOF'
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
EOF

chmod +x start_macos.sh
echo "✅ Created start_macos.sh"

# Create FastAPI standalone script
echo "📝 Creating FastAPI standalone script..."
cat > start_fastapi_macos.sh << 'EOF'
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
EOF

chmod +x start_fastapi_macos.sh
echo "✅ Created start_fastapi_macos.sh"

echo ""
echo "🎉 Installation completed successfully!"
echo "========================================"
echo ""
echo "📋 Next steps:"
echo "   1. Start Django app:     ./start_macos.sh"
echo "   2. Start FastAPI app:    ./start_fastapi_macos.sh"
echo ""
echo "🌐 Access URLs:"
echo "   Django:  http://127.0.0.1:8000"
echo "   FastAPI: http://127.0.0.1:8000/docs"
echo ""
echo "📱 Features:"
echo "   • Hair disease classification"
echo "   • Web interface"
echo "   • Metal GPU acceleration (if available)"
echo "   • User authentication"
echo ""
echo "🔧 Troubleshooting:"
echo "   • If TensorFlow fails: pip install tensorflow-macos tensorflow-metal"
echo "   • If port 8000 is busy: Change port in startup scripts"
echo "   • For issues: Check virtual environment activation"
echo ""
