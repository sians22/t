@echo off
title GGBOT v2 - Kurulum
color 0B

echo.
echo  ██████╗  ██████╗ ██████╗  ██████╗ ████████╗    ██╗   ██╗██████╗ 
echo ██╔════╝ ██╔════╝ ██╔══██╗██╔═══██╗╚══██╔══╝    ██║   ██║╚════██╗
echo ██║  ███╗██║  ███╗██████╔╝██║   ██║   ██║       ██║   ██║ █████╔╝
echo ██║   ██║██║   ██║██╔══██╗██║   ██║   ██║       ╚██╗ ██╔╝██╔═══╝ 
echo ╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝   ██║        ╚████╔╝ ███████╗
echo  ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝         ╚═══╝  ╚══════╝
echo.
echo KURULUM BASLATIILIYOR...
echo ========================
echo.

REM Yönetici yetkisi kontrolü
net session >nul 2>&1
if errorlevel 1 (
    echo [UYARI] Yonetici yetkisi gerekli!
    echo Lutfen bu dosyayi "Yonetici olarak calistir" ile acin.
    pause
    exit /b 1
)

echo [1/6] Sistem kontrol ediliyor...

REM İşletim sistemi kontrolü
ver | findstr /i "Windows" >nul
if errorlevel 1 (
    echo [HATA] Bu bot sadece Windows'ta calisir!
    pause
    exit /b 1
)

echo [BILGI] Windows sistemi tespit edildi.

REM Python kontrolü
echo [2/6] Python kontrol ediliyor...
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

REM pip kontrolü
echo [3/6] pip kontrol ediliyor...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] pip bulunamadi!
    echo Python kurulumunda bir sorun var.
    pause
    exit /b 1
)

echo [BILGI] pip hazir.

REM Gerekli klasörleri oluştur
echo [4/6] Klasor yapisi olusturuluyor...

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

REM Python kütüphanelerini yükle
echo [5/6] Python kutuphaneleri yukleniyor...
echo Bu islem birkaç dakika surebilir...

pip install --upgrade pip >nul 2>&1

echo [BILGI] Pillow yukleniyor...
pip install Pillow==10.0.1
if errorlevel 1 (
    echo [HATA] Pillow yuklenemedi!
    pause
    exit /b 1
)

echo [BILGI] pyautogui yukleniyor...
pip install pyautogui==0.9.54
if errorlevel 1 (
    echo [HATA] pyautogui yuklenemedi!
    pause
    exit /b 1
)

echo [BILGI] keyboard yukleniyor...
pip install keyboard==0.13.5
if errorlevel 1 (
    echo [HATA] keyboard yuklenemedi!
    pause
    exit /b 1
)

echo [BILGI] mouse yukleniyor...
pip install mouse==0.7.1
if errorlevel 1 (
    echo [HATA] mouse yuklenemedi!
    pause
    exit /b 1
)

echo [BILGI] psutil yukleniyor...
pip install psutil==5.9.6
if errorlevel 1 (
    echo [HATA] psutil yuklenemedi!
    pause
    exit /b 1
)

echo [BILGI] opencv-python yukleniyor...
pip install opencv-python==4.8.1.78
if errorlevel 1 (
    echo [HATA] opencv-python yuklenemedi!
    pause
    exit /b 1
)

echo [BILGI] numpy yukleniyor...
pip install numpy==1.24.3
if errorlevel 1 (
    echo [HATA] numpy yuklenemedi!
    pause
    exit /b 1
)

REM Kurulum testi
echo [6/6] Kurulum test ediliyor...

python -c "import tkinter; print('tkinter: OK')" 2>nul
if errorlevel 1 (
    echo [HATA] tkinter testi basarisiz!
    pause
    exit /b 1
)

python -c "import PIL; print('Pillow: OK')" 2>nul
if errorlevel 1 (
    echo [HATA] Pillow testi basarisiz!
    pause
    exit /b 1
)

python -c "import pyautogui; print('pyautogui: OK')" 2>nul
if errorlevel 1 (
    echo [HATA] pyautogui testi basarisiz!
    pause
    exit /b 1
)

python -c "import keyboard; print('keyboard: OK')" 2>nul
if errorlevel 1 (
    echo [HATA] keyboard testi basarisiz!
    pause
    exit /b 1
)

python -c "import mouse; print('mouse: OK')" 2>nul
if errorlevel 1 (
    echo [HATA] mouse testi basarisiz!
    pause
    exit /b 1
)

python -c "import psutil; print('psutil: OK')" 2>nul
if errorlevel 1 (
    echo [HATA] psutil testi basarisiz!
    pause
    exit /b 1
)

python -c "import cv2; print('opencv: OK')" 2>nul
if errorlevel 1 (
    echo [HATA] opencv testi basarisiz!
    pause
    exit /b 1
)

python -c "import numpy; print('numpy: OK')" 2>nul
if errorlevel 1 (
    echo [HATA] numpy testi basarisiz!
    pause
    exit /b 1
)

REM Başarılı kurulum
echo.
echo ========================================
echo           KURULUM TAMAMLANDI!
echo ========================================
echo.
echo [BASARILI] Tum kutuphaneler yuklendi.
echo [BASARILI] Klasor yapisi olusturuldu.
echo [BASARILI] Kurulum testleri gecti.
echo.
echo SONRAKI ADIMLAR:
echo 1. Mobile2 Global oyununu acin
echo 2. run_bot.bat dosyasini calistirin
echo 3. Bot arayuzunden ayarlari yapin
echo 4. "Bot Baslat" butonuna tiklayin
echo.
echo ONEMLI NOTLAR:
echo - Antivirus yazilimi bot'u engelleyebilir
echo - Bot klasorunu antivirus istisnalarina ekleyin
echo - Ilk kullanim oncesinde README.md dosyasini okuyun
echo.
echo Bot'u simdi baslatmak ister misiniz? (E/H)
set /p choice=Seciminiz: 

if /i "%choice%"=="E" (
    echo.
    echo Bot baslatiliyor...
    start run_bot.bat
) else (
    echo.
    echo Bot'u baslatmak icin run_bot.bat dosyasini calistirin.
)

echo.
echo Kurulum tamamlandi. Cikis icin bir tusa basin...
pause >nul