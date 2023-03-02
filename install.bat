@echo off
echo.
echo ^>^> Creating the venv...

python3.8 -m venv .venv

echo.
echo ^>^> Done! Installing the dependencies...
echo.

pipenv install

echo.
echo ^>^> Done!
echo.

PAUSE
