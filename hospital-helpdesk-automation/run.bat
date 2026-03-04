@echo off
echo Starting Hospital IT Helpdesk Automation System...
echo.
cd /d "%~dp0"
call venv\Scripts\activate
echo Server starting at http://localhost:8000/docs
echo Press Ctrl+C to stop the server
echo.
uvicorn src.main:app --reload
pause
