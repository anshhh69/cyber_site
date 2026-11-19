@echo off
title Ultron Launcher
echo Starting Ultron...
echo.

REM Start the file server in a new window (serves jarvis_hud.html)
start "Ultron File Server" cmd /k "python -m http.server 8000"

REM Start the app opener helper in a new window
start "Ultron App Opener" cmd /k "python ultron_opener.py"

REM Give both servers a moment to start
timeout /t 2 /nobreak >nul

REM Open Ultron in the default browser
start http://localhost:8000/jarvis_hud.html

echo Ultron is starting up. Do not close the two black windows that opened.
echo This window can be closed.
timeout /t 4
