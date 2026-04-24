@echo off
title Bas-Konus Yapay Zeka Asistan
color 0A

echo Bas-Konus Asistan baslatiliyor... Lutfen bekleyin...
echo.

:: Bu BAT dosyasının bulunduğu dizine git (Kısayol oluşturursanız sorun çıkmaması için)
cd /d "%~dp0"

:: Sanal ortamı aktive et
call venv\Scripts\activate.bat

:: Programı çalıştır
python bas_konus.py

:: Program kapanır veya çökerse hemen ekrandan kaybolmaması için açık tut
pause
