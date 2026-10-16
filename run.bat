@echo off
title AI Interviewer - Starting...
cd /d "%~dp0"

echo ==========================================
echo        AI INTERVIEWER
echo ==========================================
echo.
echo Starting virtual environment...

call venv\Scripts\activate.bat

if errorlevel 1 (
    echo.
    echo ERROR: Could not activate the virtual environment.
    echo Make sure the "venv" folder exists in this project folder.
    pause
    exit /b 1
)

echo Virtual environment activated.
echo.
echo Starting Flask server...
echo.
echo Keep this window open while using the project.
echo The browser will open automatically.
echo.

start "" "http://127.0.0.1:5000"

python app.py

echo.
echo ==========================================
echo The AI Interviewer has been stopped.
echo ==========================================
pause
