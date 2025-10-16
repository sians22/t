@echo off
title GGBOT v2 - Mobile2 Global Bot
echo GGBOT v2 - Mobile2 Global Bot Baslatiliyor...
echo.

REM Python'un yuklu olup olmadigini kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python yuklu degil!
    echo Lutfen Python 3.8+ yukleyin: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Gerekli paketleri yukle
echo Gerekli paketler yukleniyor...
pip install -r requirements.txt

REM Botu baslat
echo Bot baslatiliyor...
python main.py

pause