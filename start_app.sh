#!/bin/bash

echo "🍎 Starting Hair Disease Prediction Django App on macOS..."
echo "========================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "   Please install Python 3.8+ and try again"
    echo "   Recommended: brew install python@3.11"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Python $PYTHON_VERSION detected"

# Create and activate virtual environment
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment at $VENV_DIR ..."
    if ! python3 -m venv "$VENV_DIR"; then
        echo "⚠️ Warning: python -m venv failed. Trying virtualenv..."
        if command -v virtualenv &> /dev/null; then
            if ! virtualenv "$VENV_DIR"; then
                echo "⚠️ Warning: Failed to create virtual environment. Continuing with system Python."
            fi
        else
            echo "⚠️ Warning: virtualenv not found. Continuing with system Python."
        fi
    fi
fi

if [ -f "$VENV_DIR/bin/activate" ]; then
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    echo "✅ Virtual environment activated"
else
    echo "⚠️ Warning: Virtual environment not available; using system Python."
fi

# Upgrade pip
echo "⬆️ Upgrading pip and build tools..."
python -m pip install --upgrade pip setuptools wheel

# Install dependencies with macOS optimization
OS_NAME="$(uname -s)"
echo "🖥️ Detected OS: $OS_NAME"

echo "📚 Installing/updating dependencies..."
if [ "$OS_NAME" = "Darwin" ]; then
    # Use macOS-specific requirements for optimal performance
    if [ -f "requirements-macos.txt" ]; then
        echo "   Using macOS-optimized requirements..."
        pip install -r requirements-macos.txt
    else
        echo "   Using standard requirements..."
        pip install -r requirements.txt || true
    fi
else
    pip install -r requirements.txt
fi

# Verify TensorFlow installation on macOS
if [ "$OS_NAME" = "Darwin" ]; then
    echo "🔍 Verifying TensorFlow installation..."
    python3 -c "
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
fi

# Start the Django application
echo
echo "🚀 Starting Django application with integrated ML model..."
echo "🌐 Application will be available at: http://127.0.0.1:8000"
echo "🔮 ML Prediction page: http://127.0.0.1:8000/predict"
echo "📊 Admin panel: http://127.0.0.1:8000/admin"
echo "========================================================"
python3 start_django_app.py
