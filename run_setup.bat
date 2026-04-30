@echo off
cd "c:\Users\HP\OneDrive\Documents\new project election"
echo.
echo ========================================
echo Setting up Election Assistant
echo ========================================
echo.
echo Step 1: Installing dependencies...
call venv\Scripts\pip.exe install -r requirements.txt
echo.
echo Step 2: Running migrations...
call venv\Scripts\python.exe manage.py migrate
echo.
echo Step 3: Starting Django server...
echo.
echo Server will be available at:
echo   http://127.0.0.1:8000
echo.
call venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
