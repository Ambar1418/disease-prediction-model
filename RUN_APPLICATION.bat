@echo off
title Hair Disease Prediction Application
echo ================================================
echo    Hair Disease Prediction Application
echo ================================================
echo.
echo This application requires Python to be installed.
echo.
echo Checking Python installation...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found! Checking dependencies...

REM Check if required packages are installed
python -c "import django, tensorflow, PIL, numpy" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    echo This may take a few minutes...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Please check your internet connection and try again
        pause
        exit /b 1
    )
)

echo.
echo Starting Hair Disease Prediction Application...
echo.
echo The application will open in your web browser
echo at: http://127.0.0.1:8000
echo.
echo Press Ctrl+C in this window to stop the application
echo ================================================
echo.

REM Run the application
python main_exe.py

echo.
echo Application has stopped.
pause
