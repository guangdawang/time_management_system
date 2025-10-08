@echo off
chcp 65001 > nul
title Time Management System Packager
echo =======================================
echo      Time Management System Packager
echo =======================================
echo.

echo Step 1: Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Step 2: Installing packaging dependencies...
pip install pyinstaller

echo Step 3: Starting build process...
python build_windows.py

echo.
echo =======================================
echo   Build completed! Check dist folder
echo =======================================
echo.
pause