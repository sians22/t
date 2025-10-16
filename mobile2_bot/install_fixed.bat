@echo off
title GGBOT v2 - Gelişmiş Kurulum
color 0B

echo.
echo  ██████╗  ██████╗ ██████╗  ██████╗ ████████╗    ██╗   ██╗██████╗ 
echo ██╔════╝ ██╔════╝ ██╔══██╗██╔═══██╗╚══██╔══╝    ██║   ██║╚════██╗
echo ██║  ███╗██║  ███╗██████╔╝██║   ██║   ██║       ██║   ██║ █████╔╝
echo ██║   ██║██║   ██║██╔══██╗██║   ██║   ██║       ╚██╗ ██╔╝██╔═══╝ 
echo ╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝   ██║        ╚████╔╝ ███████╗
echo  ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝         ╚═══╝  ╚══════╝
echo.
echo GELISMIS KURULUM BASLATIILIYOR...
echo ==================================
echo.

REM Yönetici yetkisi kontrolü
net session >nul 2>&1
if errorlevel 1 (
    echo [UYARI] Yonetici yetkisi gerekli!
    echo Lutfen bu dosyayi "Yonetici olarak calistir" ile acin.
    pause
    exit /b 1
)

echo [1/7] Sistem kontrol ediliyor...

REM İşletim sistemi kontrolü
ver | findstr /i "Windows" >nul
if errorlevel 1 (
    echo [HATA] Bu bot sadece Windows'ta calisir!
    pause
    exit /b 1
)

echo [BILGI] Windows sistemi tespit edildi.

REM Python kontrolü
echo [2/7] Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi!
    echo.
    echo Python kurulumu gerekli:
    echo 1. https://www.python.org/downloads/ adresine gidin
    echo 2. Python 3.8+ surumunu indirin
    echo 3. Kurulum sirasinda "Add Python to PATH" secenegini isaretleyin
    echo 4. Kurulumu tamamlayin ve bu dosyayi tekrar calistirin
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [BILGI] Python %PYTHON_VERSION% bulundu.

REM pip kontrolü ve güncelleme
echo [3/7] pip kontrol ediliyor ve guncelleniyor...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] pip bulunamadi!
    echo Python kurulumunda bir sorun var.
    pause
    exit /b 1
)

echo [BILGI] pip guncelleniyor...
python -m pip install --upgrade pip >nul 2>&1

REM Gerekli klasörleri oluştur
echo [4/7] Klasor yapisi olusturuluyor...

if not exist "config" (
    mkdir config
    echo [BILGI] config klasoru olusturuldu.
)

if not exist "config\routes" (
    mkdir config\routes
    echo [BILGI] routes klasoru olusturuldu.
)

if not exist "config\items" (
    mkdir config\items
    echo [BILGI] items klasoru olusturuldu.
)

if not exist "logs" (
    mkdir logs
    echo [BILGI] logs klasoru olusturuldu.
)

if not exist "assets" (
    mkdir assets
    echo [BILGI] assets klasoru olusturuldu.
)

if not exist "assets\templates" (
    mkdir assets\templates
    echo [BILGI] templates klasoru olusturuldu.
)

if not exist "backup" (
    mkdir backup
    echo [BILGI] backup klasoru olusturuldu.
)

REM Temel kütüphaneleri yükle (sorunsuz olanlar)
echo [5/7] Temel kutuphaneler yukleniyor...

echo [BILGI] Pillow yukleniyor...
pip install Pillow==10.0.1 --no-warn-script-location
if errorlevel 1 (
    echo [UYARI] Pillow yuklenemedi, alternatif deneniyor...
    pip install Pillow --no-warn-script-location
)

echo [BILGI] numpy yukleniyor...
pip install numpy==1.24.3 --no-warn-script-location
if errorlevel 1 (
    echo [UYARI] numpy yuklenemedi, alternatif deneniyor...
    pip install numpy --no-warn-script-location
)

echo [BILGI] psutil yukleniyor...
pip install psutil==5.9.6 --no-warn-script-location
if errorlevel 1 (
    echo [UYARI] psutil yuklenemedi, alternatif deneniyor...
    pip install psutil --no-warn-script-location
)

REM Problemli kütüphaneler için özel yükleme
echo [6/7] Gelismis kutuphaneler yukleniyor...

echo [BILGI] pyautogui yukleniyor...
pip install pyautogui --no-warn-script-location
if errorlevel 1 (
    echo [UYARI] pyautogui yuklenemedi, manuel kurulum gerekebilir.
)

echo [BILGI] keyboard yukleniyor...
pip install keyboard --no-warn-script-location
if errorlevel 1 (
    echo [UYARI] keyboard yuklenemedi, manuel kurulum gerekebilir.
)

echo [BILGI] mouse yukleniyor...
pip install mouse --no-warn-script-location
if errorlevel 1 (
    echo [UYARI] mouse yuklenemedi, manuel kurulum gerekebilir.
)

echo [BILGI] opencv-python yukleniyor...
pip install opencv-python --no-warn-script-location
if errorlevel 1 (
    echo [UYARI] opencv-python yuklenemedi, manuel kurulum gerekebilir.
)

REM Windows özel kütüphaneler (opsiyonel)
echo [BILGI] Windows kutuphaneleri yukleniyor (opsiyonel)...
pip install pywin32 --no-warn-script-location >nul 2>&1
if errorlevel 1 (
    echo [UYARI] pywin32 yuklenemedi, bazi ozellikler calismayabilir.
    echo [BILGI] Bu normal bir durum, bot yine de calisacak.
)

REM Kurulum testi
echo [7/7] Kurulum test ediliyor...

echo [BILGI] Temel modulleri test ediliyor...

python -c "import sys; print('Python:', sys.version)" 2>nul
if errorlevel 1 (
    echo [HATA] Python testi basarisiz!
)

python -c "import tkinter; print('tkinter: OK')" 2>nul
if errorlevel 1 (
    echo [UYARI] tkinter bulunamadi, GUI calismayabilir.
) else (
    echo [BILGI] tkinter: OK
)

python -c "import json, time, threading, os; print('Temel moduller: OK')" 2>nul
if errorlevel 1 (
    echo [HATA] Temel moduller testi basarisiz!
) else (
    echo [BILGI] Temel moduller: OK
)

REM Opsiyonel modül testleri
python -c "import PIL; print('Pillow: OK')" 2>nul || echo [UYARI] Pillow yuklu degil
python -c "import numpy; print('numpy: OK')" 2>nul || echo [UYARI] numpy yuklu degil
python -c "import psutil; print('psutil: OK')" 2>nul || echo [UYARI] psutil yuklu degil

REM Bot testi
echo [BILGI] Bot modullerini test ediliyor...
python -c "from src.config.settings import Settings; print('Settings: OK')" 2>nul
if errorlevel 1 (
    echo [UYARI] Bot modulleri tam yuklu degil, yine de calisabilir.
) else (
    echo [BILGI] Bot modulleri: OK
)

echo.
echo ========================================
echo           KURULUM TAMAMLANDI!
echo ========================================
echo.
echo [BASARILI] Temel kurulum tamamlandi.
echo [BILGI] Bazi kutuphaneler yuklenemis olabilir, bu normal.
echo [BILGI] Bot yine de calisacak, eksik ozellikler devre disi kalacak.
echo.
echo SONRAKI ADIMLAR:
echo 1. Mobile2 Global oyununu acin
echo 2. run_bot.bat dosyasini calistirin
echo 3. Eger GUI acilmazsa demo.py calistirin
echo.
echo ALTERNATIF CALISMA MODLARI:
echo - GUI Modu: python main.py
echo - Demo Modu: python demo.py
echo - Batch Dosyasi: run_bot.bat
echo.
echo ONEMLI NOTLAR:
echo - Antivirus yazilimi bot'u engelleyebilir
echo - Bot klasorunu antivirus istisnalarina ekleyin
echo - Ilk kullanim oncesinde README.md dosyasini okuyun
echo - Bazi ozellikler Windows'a ozel kutuphaneler gerektirir
echo.

echo Bot'u simdi baslatmak ister misiniz? (E/H)
set /p choice=Seciminiz: 

if /i "%choice%"=="E" (
    echo.
    echo Bot baslatiliyor...
    echo Eger GUI acilmazsa, demo modu calisacak...
    
    REM Önce GUI modunu dene
    python main.py
    if errorlevel 1 (
        echo.
        echo GUI modu calismadi, demo modu baslatiliyor...
        python demo.py
    )
) else (
    echo.
    echo Bot'u baslatmak icin:
    echo - GUI icin: python main.py
    echo - Demo icin: python demo.py
    echo - Batch icin: run_bot.bat
)

echo.
echo Kurulum tamamlandi. Cikis icin bir tusa basin...
pause >nul