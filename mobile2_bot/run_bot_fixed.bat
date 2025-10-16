@echo off
title GGBOT v2 - Mobile2 Global Bot (Gelismis)
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

REM Gerekli klasörleri oluştur
if not exist "config" mkdir config
if not exist "config\routes" mkdir config\routes
if not exist "config\items" mkdir config\items
if not exist "logs" mkdir logs
if not exist "assets" mkdir assets
if not exist "assets\templates" mkdir assets\templates
if not exist "backup" mkdir backup

echo [BILGI] Klasor yapisi hazir.

REM Bot modüllerini kontrol et
echo [BILGI] Bot modulleri kontrol ediliyor...
python -c "from src.config.settings import Settings; print('Bot modulleri: OK')" >nul 2>&1
if errorlevel 1 (
    echo [UYARI] Bot modulleri tam yuklu degil.
    echo Demo modu calistirilacak...
    goto DEMO_MODE
)

echo [BILGI] Bot modulleri hazir.

REM GUI modunu dene
echo [BILGI] GUI modu deneniyor...
python -c "import tkinter; print('GUI: OK')" >nul 2>&1
if errorlevel 1 (
    echo [UYARI] GUI kutuphaneleri bulunamadi.
    echo Demo modu calistirilacak...
    goto DEMO_MODE
)

echo [BILGI] GUI kutuphaneleri hazir.

REM Ana bot'u çalıştır
echo [BILGI] GGBOT v2 GUI modu baslatiliyor...
echo.
echo Hotkey'ler:
echo F9  - Bot Baslat/Durdur
echo F10 - Bot Duraklat/Devam
echo F11 - Acil Durdurma
echo.
echo Bot penceresi acilacak...
echo.

python main.py

REM Hata durumunda demo moduna geç
if errorlevel 1 (
    echo.
    echo [UYARI] GUI modu calismadi!
    echo Demo modu baslatiliyor...
    goto DEMO_MODE
)

goto END

:DEMO_MODE
echo.
echo ========================================
echo           DEMO MODU BASLATILIYOR
echo ========================================
echo.
echo GUI modu calismadigi icin demo modu baslatiliyor.
echo Bu mod temel bot fonksiyonlarini test etmenizi saglar.
echo.
echo Demo'yu durdurmak icin Ctrl+C basin.
echo.

python demo.py

if errorlevel 1 (
    echo.
    echo [HATA] Demo modu da calismadi!
    echo Lutfen kurulum dosyalarini kontrol edin.
    echo.
    echo Manuel calistirma:
    echo python main.py    (GUI icin)
    echo python demo.py    (Demo icin)
)

:END
echo.
echo Bot kapatildi. Cikis icin bir tusa basin...
pause >nul