#!/usr/bin/env python3
"""
Comprehensive build script that tries multiple approaches to create executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if all required files exist"""
    print("🔍 Checking project requirements...")
    
    required_files = [
        "minor/manage.py",
        "minor/myapp/ml_service.py", 
        "hair-diseases.h5"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def install_build_tools():
    """Install required build tools"""
    print("🔧 Installing build tools...")
    
    tools = ["pyinstaller", "cx_freeze"]
    
    for tool in tools:
        try:
            print(f"Installing {tool}...")
            subprocess.run([sys.executable, "-m", "pip", "install", tool], 
                         check=True, capture_output=True)
            print(f"✅ {tool} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {tool}: {e}")
            return False
    
    return True

def try_pyinstaller():
    """Try building with PyInstaller"""
    print("🔨 Attempting build with PyInstaller...")
    
    try:
        # Clean previous builds
        for dir_name in ["build", "dist"]:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
        
        # Run PyInstaller
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "HairDiseasePrediction.spec"]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        if os.path.exists("dist/HairDiseasePrediction.exe"):
            print("✅ PyInstaller build successful!")
            return True
        else:
            print("❌ PyInstaller build failed - no executable created")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller build failed: {e}")
        return False

def try_cx_freeze():
    """Try building with cx_Freeze"""
    print("🔨 Attempting build with cx_Freeze...")
    
    try:
        # Clean previous builds
        if os.path.exists("dist_cx_freeze"):
            shutil.rmtree("dist_cx_freeze")
        
        # Run cx_Freeze
        cmd = [sys.executable, "setup_cx_freeze.py", "build"]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        exe_path = "dist_cx_freeze/HairDiseasePrediction.exe"
        if os.path.exists(exe_path):
            print("✅ cx_Freeze build successful!")
            return True
        else:
            print("❌ cx_Freeze build failed - no executable created")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ cx_Freeze build failed: {e}")
        return False

def create_simple_executable():
    """Create a simple executable using auto-py-to-exe"""
    print("🔨 Attempting build with auto-py-to-exe...")
    
    try:
        # Install auto-py-to-exe
        subprocess.run([sys.executable, "-m", "pip", "install", "auto-py-to-exe"], 
                      check=True, capture_output=True)
        
        print("📝 Creating auto-py-to-exe configuration...")
        
        # Create a simple config
        config = {
            "version": "auto-py-to-exe-configuration_v1",
            "pyinstallerOptions": {
                "filenames": ["main_exe.py"],
                "onefile": True,
                "console": True,
                "name": "HairDiseasePrediction"
            }
        }
        
        import json
        with open("auto_py_to_exe_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuration created. Please run auto-py-to-exe manually:")
        print("   auto-py-to-exe")
        print("   Then load the config file: auto_py_to_exe_config.json")
        
        return True
        
    except Exception as e:
        print(f"❌ auto-py-to-exe setup failed: {e}")
        return False

def create_portable_version():
    """Create a portable version that can run without installation"""
    print("📦 Creating portable version...")
    
    try:
        # Create portable directory
        portable_dir = "HairDiseasePrediction_Portable"
        if os.path.exists(portable_dir):
            shutil.rmtree(portable_dir)
        
        os.makedirs(portable_dir)
        
        # Copy necessary files
        files_to_copy = [
            "main_exe.py",
            "requirements.txt",
            "README_EXECUTABLE.md"
        ]
        
        dirs_to_copy = [
            "minor",
            "frontend"
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, portable_dir)
        
        for dir_name in dirs_to_copy:
            if os.path.exists(dir_name):
                shutil.copytree(dir_name, os.path.join(portable_dir, dir_name))
        
        # Copy model file
        if os.path.exists("hair-diseases.h5"):
            shutil.copy2("hair-diseases.h5", portable_dir)
        
        # Create run script
        run_script = '''@echo off
echo Hair Disease Prediction - Portable Version
echo ==========================================
echo.
echo This is a portable version that requires Python to be installed.
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting application...
python main_exe.py
pause
'''
        
        with open(os.path.join(portable_dir, "run.bat"), "w") as f:
            f.write(run_script)
        
        print(f"✅ Portable version created: {portable_dir}")
        print("   To use: Extract to any folder and run run.bat")
        
        return True
        
    except Exception as e:
        print(f"❌ Portable version creation failed: {e}")
        return False

def main():
    """Main build function"""
    print("🏥 Hair Disease Prediction - Comprehensive Executable Builder")
    print("=" * 70)
    
    # Check requirements
    if not check_requirements():
        input("Press Enter to exit...")
        return False
    
    # Install build tools
    if not install_build_tools():
        input("Press Enter to exit...")
        return False
    
    success_count = 0
    
    # Try PyInstaller
    if try_pyinstaller():
        success_count += 1
    
    # Try cx_Freeze
    if try_cx_freeze():
        success_count += 1
    
    # Create portable version
    if create_portable_version():
        success_count += 1
    
    # Setup auto-py-to-exe
    create_simple_executable()
    
    print("=" * 70)
    if success_count > 0:
        print(f"🎉 Build completed! {success_count} executable(s) created successfully!")
        print("\nAvailable executables:")
        
        if os.path.exists("dist/HairDiseasePrediction.exe"):
            print("  📁 PyInstaller: dist/HairDiseasePrediction.exe")
        
        if os.path.exists("dist_cx_freeze/HairDiseasePrediction.exe"):
            print("  📁 cx_Freeze: dist_cx_freeze/HairDiseasePrediction.exe")
        
        if os.path.exists("HairDiseasePrediction_Portable"):
            print("  📁 Portable: HairDiseasePrediction_Portable/")
        
        print("\n📖 Documentation: README_EXECUTABLE.md")
    else:
        print("❌ No executables were created successfully")
        print("💡 Try the portable version or manual PyInstaller setup")
    
    print("=" * 70)
    
    return success_count > 0

if __name__ == "__main__":
    success = main()
    if not success:
        input("Press Enter to exit...")
        sys.exit(1)
