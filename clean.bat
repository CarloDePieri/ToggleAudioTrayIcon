@echo off

echo.
echo ^>^> Cleaning...
echo.

del ToggleAudioTrayIcon.spec
RMDIR /S /Q dist

echo ^>^> Done!
echo.

PAUSE
