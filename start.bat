@echo off
REM PaperBOT Startup Script for Windows

echo ========================================
echo  PaperBOT - AI Research Assistant
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then run: venv\Scripts\activate
    echo Then run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo.
    echo [WARNING] .env file not found!
    echo Please copy .env.example to .env and configure your API keys
    echo.
    pause
)

REM Start the application
echo [2/3] Starting PaperBOT server...
echo.
echo Server will start at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
echo [3/3] Running application...
echo.

python app.py

pause
