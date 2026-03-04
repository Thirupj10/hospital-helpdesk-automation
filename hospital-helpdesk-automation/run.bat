@echo off
echo Starting Hospital IT Helpdesk Automation System...
echo.

cd /d "D:\PROJECTS DONE FOR SION AND STRYKER\hospital-helpdesk-automation\hospital-helpdesk-automation"

call venv\Scripts\activate.bat

echo Server starting at http://localhost:8000/docs
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn src.main:app --reload
pause
