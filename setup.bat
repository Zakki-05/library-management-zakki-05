@echo off
echo ==========================================
echo Setting up Library Management System
echo ==========================================
echo.

echo [1/5] Creating Python Virtual Environment...
python -m venv venv

echo [2/5] Activating Virtual Environment and Installing Dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo [3/5] Running Database Migrations...
python manage.py makemigrations
python manage.py migrate

echo [4/5] Populating Database with Initial Data...
python populate_data.py

echo.
echo ==========================================
echo [5/5] Setup Complete! Starting Server...
echo ==========================================
echo.
echo The server will start now. 
echo Please go to http://127.0.0.1:8000 in your browser.
echo.
python manage.py runserver
pause
