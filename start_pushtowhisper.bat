@echo off
title PushToWhisper AI Assistant
color 0A

echo PushToWhisper is starting... Please wait...
echo.

:: Dosyayı nereye taşırsanız taşıyın her zaman doğru klasöre gitmesini sağlar
cd /d "C:\Users\burak\Desktop\python\bas_konus"

:: Sanal ortamı aktive et
call venv\Scripts\activate.bat

:: Programı çalıştır
python pushtowhisper.py

:: Program kapanır veya çökerse hemen ekrandan kaybolmaması için açık tut
pause
