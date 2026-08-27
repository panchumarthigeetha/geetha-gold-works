@echo off
cd /d "%~dp0"
echo Stopping old website and public link...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5500" ^| findstr "LISTENING"') do taskkill /F /PID %%a >nul 2>&1
taskkill /F /IM cloudflared.exe >nul 2>&1
timeout /t 2 /nobreak >nul
powershell -ExecutionPolicy Bypass -File "%~dp0start-public.ps1"
pause
