@echo off
echo ================================================
echo Hair Disease Prediction - Executable Builder
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Python found. Starting build process...
echo.

REM Run the build script
python build_exe.py

if errorlevel 1 (
    echo.
    echo Build failed! Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ================================================
echo Build completed successfully!
echo ================================================
echo.
echo Your executable is ready at: dist\HairDiseasePrediction.exe
echo.
echo To test the executable:
echo 1. Navigate to the dist folder
echo 2. Double-click HairDiseasePrediction.exe
echo 3. The application will start and open in your browser
echo.
pause
