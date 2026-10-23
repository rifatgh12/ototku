@echo off
title OtotKu - Server Lokal Multi-Device
chcp 65001 >nul
color 0b

echo ================================================================
echo         OTOTKU FITNESS TRACKER - PENGATURAN SERVER
echo ================================================================
echo Memeriksa instalasi Python...

python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Python belum terdeteksi di komputer ini!
    echo Silakan instal Python dari https://www.python.org/downloads/
    echo dan pastikan centang opsi "Add python.exe to PATH" saat instalasi.
    echo.
    pause
    exit /b
)

echo Python terdeteksi. Memulai server...
echo.

:: Jalankan script server python
python serve.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Server terhenti atau terjadi kendala.
    pause
)
