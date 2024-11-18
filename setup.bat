@echo off

REM Get the absolute path of the current directory
SET "BASE_DIR=%cd%"

REM Change directory to frontend and install npm packages
cd /d "%BASE_DIR%\frontend"
npm install

REM Change back to root directory
cd /d "%BASE_DIR%"

REM Change directory to backend and set up virtual environment
cd /d "%BASE_DIR%\backend"
python -m venv venv  REM Use python instead of python3
call venv\Scripts\activate.bat  REM Activate venv
pip install -r requirements.txt
call venv\Scripts\deactivate.bat  REM Deactivate venv

REM Change back to root directory
cd /d "%BASE_DIR%"

REM Open a new terminal for frontend
start cmd /k "cd /d \"%BASE_DIR%\frontend\" && npm start"

REM Open another new terminal for backend
start cmd /k "cd /d \"%BASE_DIR%\backend\" && call venv\Scripts\activate.bat && python manage.py runserver"

echo All setup complete. Use the opened terminals for running frontend and backend servers.
