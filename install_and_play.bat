@echo off
title Murder at Blackwood Manor
py -m pip install pygame
if errorlevel 1 goto error
py blackwood_manor.py
exit /b 0
:error
echo Please confirm Python is installed.
pause
