@echo off
cd /d "%~dp0"

py -3 start.py
if errorlevel 9009 python start.py

pause
