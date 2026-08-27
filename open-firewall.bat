@echo off
echo Opening port 5500 for Geetha Gold Works website...
netsh advfirewall firewall delete rule name="Geetha Gold Works Website" >nul 2>&1
netsh advfirewall firewall add rule name="Geetha Gold Works Website" dir=in action=allow protocol=TCP localport=5500
if %errorlevel%==0 (
  echo Done. Other devices on your Wi-Fi can now open the admin page.
) else (
  echo Failed. Right-click this file and choose "Run as administrator".
)
pause
