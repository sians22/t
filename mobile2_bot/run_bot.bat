@echo off
title GGBOT v2 - Mobile2 Global Bot
color 0A

echo.
echo  ██████╗  ██████╗ ██████╗  ██████╗ ████████╗    ██╗   ██╗██████╗ 
echo ██╔════╝ ██╔════╝ ██╔══██╗██╔═══██╗╚══██╔══╝    ██║   ██║╚════██╗
echo ██║  ███╗██║  ███╗██████╔╝██║   ██║   ██║       ██║   ██║ █████╔╝
echo ██║   ██║██║   ██║██╔══██╗██║   ██║   ██║       ╚██╗ ██╔╝██╔═══╝ 
echo ╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝   ██║        ╚████╔╝ ███████╗
echo  ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝         ╚═══╝  ╚══════╝
echo.
echo Mobile2 Global Bot - Ogretmen Odevi
echo ====================================
echo.

REM Python'un kurulu olup olmadığını kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi!
    echo Lutfen Python 3.8+ kurdugunuzdan emin olun.
    echo Indirme linki: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [BILGI] Python bulundu.

REM Gerekli kütüphaneleri kontrol et
echo [BILGI] Gerekli kutuphaneler kontrol ediliyor...
python -c "import tkinter, PIL, pyautogui, keyboard, mouse, psutil, cv2, numpy" >nul 2>&1
if errorlevel 1 (
    echo [UYARI] Bazi kutuphaneler eksik. Yukleniyor...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [HATA] Kutuphaneler yuklenemedi!
        echo Lutfen manuel olarak yuklemeyi deneyin:
        echo pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo [BILGI] Tum kutuphaneler hazir.

REM Config klasörünü oluştur
if not exist "config" mkdir config
if not exist "config\routes" mkdir config\routes
if not exist "config\items" mkdir config\items
if not exist "logs" mkdir logs
if not exist "assets" mkdir assets
if not exist "assets\templates" mkdir assets\templates
if not exist "backup" mkdir backup

echo [BILGI] Klasor yapisi hazir.

REM Bot'u başlat
echo [BILGI] GGBOT v2 baslatiliyor...
echo.
echo Hotkey'ler:
echo F9  - Bot Baslat/Durdur
echo F10 - Bot Duraklat/Devam
echo F11 - Acil Durdurma
echo.
echo Bot penceresi acilacak...
echo.

python main.py

REM Hata durumunda
if errorlevel 1 (
    echo.
    echo [HATA] Bot beklenmedik bir sekilde kapandi!
    echo Log dosyalarini kontrol edin: logs\bot.log
    echo.
)

echo.
echo Bot kapatildi. Cikis icin bir tusa basin...
pause >nul