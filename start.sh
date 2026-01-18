#!/bin/bash
# PaperBOT Startup Script for Linux/Mac

echo "========================================"
echo " PaperBOT - AI Research Assistant"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    echo "Then run: source venv/bin/activate"
    echo "Then run: pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "[1/3] Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "[WARNING] .env file not found!"
    echo "Please copy .env.example to .env and configure your API keys"
    echo ""
    read -p "Press enter to continue..."
fi

# Start the application
echo "[2/3] Starting PaperBOT server..."
echo ""
echo "Server will start at: http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""
echo "[3/3] Running application..."
echo ""

python app.py
