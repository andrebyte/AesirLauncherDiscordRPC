@echo off
title Aesir Launcher Universal RPC
color 0b

echo ==================================================
echo   AESIR LAUNCHER UNIVERSAL RPC ARKA PLANDA BASLIYOR
echo ==================================================
echo.

:: Python yuklu mu kontrol et
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [HATA] Python sisteminizde yuklu degil veya PATH'e eklenmemis!
    echo Lutfen Python'u yukleyin: https://www.python.org/
    pause
    exit
)

:: Scripti gizli (pythonw) olarak calistir
echo [+] Universal RPC arka planda baslatildi...
echo [+] Kapatmak icin Gorev Yoneticisinden "pythonw.exe" islemini sonlandirin.
echo.
start "" pythonw universal_rpc.py

timeout /t 3 >nul
exit
