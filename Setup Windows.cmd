@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" goto install
where py >nul 2>nul
if not errorlevel 1 (
  py -3 -m venv .venv
) else (
  python -m venv .venv
)
if errorlevel 1 goto failed
:install
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed
echo.
echo Setup complete. Double-click Launch integrated story.cmd to start.
pause
exit /b 0
:failed
echo.
echo Setup did not finish. Check Python 3.11+ and your internet connection.
echo See START_HERE.md for manual instructions.
pause
exit /b 1
