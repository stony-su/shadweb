@echo off
echo HEIC to JPG Converter Setup
echo ===========================

echo Installing required packages...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error installing packages. Please make sure Python and pip are installed.
    pause
    exit /b 1
)

echo.
echo Running HEIC to JPG converter...
python heic_to_jpg_converter.py

echo.
echo Press any key to exit...
pause >nul 