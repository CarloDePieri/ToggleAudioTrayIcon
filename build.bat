@echo off
echo.
echo ^>^> Starting build process...
mkdir dist\ >NUL
@echo on
pipenv run pyinstaller --noconsole -F -n "ToggleAudioTrayIcon" -i "icon.ico" --distpath "dist/ToggleAudioTrayIcon" toggle_app.py
@echo off
RMDIR /S /Q build
copy headset.png dist\ToggleAudioTrayIcon\ >NUL
copy screen.png dist\ToggleAudioTrayIcon\ >NUL
copy config.ini dist\ToggleAudioTrayIcon\ >NUL

echo.
echo ^>^> Built files are in the dist\ToggleAudioTrayIcon folder!
echo.

PAUSE