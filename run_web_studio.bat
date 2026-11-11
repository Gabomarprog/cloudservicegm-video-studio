@echo off
cd /d "%~dp0"
py -3 studio_server.py
if errorlevel 1 (
  echo.
  echo No se pudo iniciar cloudservicegm Video Studio.
  echo Comprueba que Python 3 este instalado.
  pause
)
