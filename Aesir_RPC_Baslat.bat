@echo off
title Aesir Launcher Discord RPC - Calistirici
color 0b

echo ==================================================
echo      AESIR LAUNCHER DISCORD RPC BASLATILIYOR
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

:: Scripti calistir
echo [+] Discord RPC Izleyici baslatildi...
echo [+] Bu pencereyi kapatirsaniz RPC durur.
echo.
python aesir_watcher.py

if %errorlevel% neq 0 (
    echo.
    echo [HATA] Script calisirken bir sorun olustu!
    pause
)

echo.
echo [!] Script sonlandirildi.
pause
