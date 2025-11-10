#!/usr/bin/env python3
"""
macOS Setup Test Script for Hair Disease Prediction Model
This script tests all components of the macOS-optimized setup
"""

import os
import sys
import subprocess
from pathlib import Path

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible (requires 3.8+)")
        return False

def test_tensorflow():
    """Test TensorFlow installation and Metal GPU support"""
    print("🤖 Testing TensorFlow installation...")
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__} installed successfully")
        
        # Test Metal GPU support
        if sys.platform == "darwin":
            devices = tf.config.list_physical_devices()
            gpu_devices = [d for d in devices if 'GPU' in d.name]
            if gpu_devices:
                print(f"✅ Metal GPU acceleration available: {len(gpu_devices)} device(s)")
                for device in gpu_devices:
                    print(f"   - {device.name}")
            else:
                print("⚠️ No Metal GPU detected (CPU-only mode)")
        
        return True
    except ImportError as e:
        print(f"❌ TensorFlow import failed: {e}")
        return False
    except Exception as e:
        print(f"⚠️ TensorFlow test warning: {e}")
        return True

def test_django():
    """Test Django installation"""
    print("🌐 Testing Django installation...")
    try:
        import django
        print(f"✅ Django {django.get_version()} installed successfully")
        return True
    except ImportError as e:
        print(f"❌ Django import failed: {e}")
        return False

def test_fastapi():
    """Test FastAPI installation"""
    print("🚀 Testing FastAPI installation...")
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__} installed successfully")
        return True
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False

def test_model_loading():
    """Test ML model loading"""
    print("🧠 Testing ML model loading...")
    try:
        # Test Django ML service
        sys.path.insert(0, str(Path(__file__).parent / "minor"))
        from myapp.ml_service import ml_service
        
        if ml_service.model is not None:
            print("✅ Django ML service model loaded successfully")
        else:
            print("❌ Django ML service model failed to load")
            return False
        
        # Test FastAPI model loading
        from main import model
        if model is not None:
            print("✅ FastAPI model loaded successfully")
        else:
            print("❌ FastAPI model failed to load")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Model loading test failed: {e}")
        return False

def test_file_structure():
    """Test required file structure"""
    print("📁 Testing file structure...")
    required_files = [
        "hair-diseases.h5",
        "requirements-macos.txt",
        "start_app.sh",
        "start_django_app.py",
        "main.py",
        "minor/manage.py",
        "minor/myapp/ml_service.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_scripts():
    """Test startup scripts"""
    print("📜 Testing startup scripts...")
    scripts = ["start_app.sh", "start_macos.sh", "start_fastapi_macos.sh"]
    
    for script in scripts:
        if os.path.exists(script):
            if os.access(script, os.X_OK):
                print(f"✅ {script} is executable")
            else:
                print(f"⚠️ {script} exists but is not executable")
        else:
            print(f"❌ {script} not found")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🍎 Hair Disease Prediction - macOS Setup Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("File Structure", test_file_structure),
        ("Scripts", test_scripts),
        ("TensorFlow", test_tensorflow),
        ("Django", test_django),
        ("FastAPI", test_fastapi),
        ("Model Loading", test_model_loading),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! macOS setup is ready.")
        print("\n📋 Next steps:")
        print("   1. Start Django app:     ./start_macos.sh")
        print("   2. Start FastAPI app:    ./start_fastapi_macos.sh")
        print("   3. Access Django:         http://127.0.0.1:8000")
        print("   4. Access FastAPI docs:   http://127.0.0.1:8000/docs")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
