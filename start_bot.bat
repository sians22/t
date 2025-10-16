@echo off
title Mobile2 Global Bot Launcher
echo Starting Mobile2 Global Bot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Run the launcher
python launcher.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Bot encountered an error!
    pause
)