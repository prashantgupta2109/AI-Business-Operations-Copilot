@echo off
title AI Business Operations Copilot

echo ============================================
echo   AI Business Operations Copilot
echo ============================================
echo.

REM --- Start Backend in a new terminal window ---
echo [1/2] Starting Backend (FastAPI on port 8000)...
start "AI Copilot - Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --port 8000"

REM --- Wait 5 seconds for backend to initialize ---
timeout /t 5 /nobreak >nul

REM --- Start Frontend in a new terminal window ---
echo [2/2] Starting Frontend (Streamlit on port 8501)...
start "AI Copilot - Frontend" cmd /k "cd /d %~dp0frontend && python -m streamlit run app.py --server.port 8501"

REM --- Wait for Streamlit to start, then open browser ---
timeout /t 6 /nobreak >nul

echo.
echo ============================================
echo   Both servers are starting up!
echo   Backend  : http://localhost:8000
echo   Frontend : http://localhost:8501
echo   API Docs : http://localhost:8000/docs
echo ============================================
echo.

start http://localhost:8501

echo Done! Your browser should open automatically.
echo Close the two terminal windows to stop the servers.
pause
