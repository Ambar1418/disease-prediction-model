@echo off
echo Starting Hair Disease Prediction Django App...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Installing/updating dependencies...
pip install -r requirements.txt

REM Start the Django application
echo.
echo Starting Django application with integrated ML model...
python start_django_app.py

pause
