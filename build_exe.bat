@echo off
title Build Blackwood Manor EXE
echo Installing the EXE builder and sound engine...
py -m pip install --upgrade pyinstaller pygame
if errorlevel 1 goto error

echo.
echo Building Blackwood_Manor.exe...
py -m PyInstaller --noconfirm --clean --onefile --windowed --name Murder_at_the_Blackwood_Manor --add-data "assets;assets" --add-data "sounds;sounds" blackwood_manor.py
if errorlevel 1 goto error

echo.
echo SUCCESS!
echo Your executable is here:
echo %CD%\dist\Murder_at_the_Blackwood_Manor.exe
pause
exit /b 0

:error
echo.
echo The build did not complete. Check that Python is installed and connected to the internet.
pause
exit /b 1
