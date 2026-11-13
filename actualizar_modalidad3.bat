@echo off
setlocal
cd /d "%~dp0"
title cloudservicegm - Actualizar modalidad 3

echo.
echo ==============================================
echo   Actualizador de cloudservicegm - Modalidad 3
echo ==============================================
echo.
echo Descargando solamente el servidor actualizado...
curl.exe --fail --location --silent --show-error --retry 3 --retry-delay 2 ^
  --output "manual_studio_server.py.new" ^
  "https://raw.githubusercontent.com/Gabomarprog/cloudservicegm-video-studio/main/manual_studio_server.py"
if errorlevel 1 (
  echo.
  echo ERROR: No se pudo descargar el actualizador desde GitHub.
  del /q "manual_studio_server.py.new" 2>nul
  pause
  exit /b 1
)

echo Comprobando sintaxis del archivo descargado...
python -c "from pathlib import Path; p=Path('manual_studio_server.py.new'); compile(p.read_text(encoding='utf-8'), 'manual_studio_server.py', 'exec')"
if errorlevel 1 (
  echo.
  echo ERROR: El archivo descargado no paso la comprobacion. No se reemplazo nada.
  del /q "manual_studio_server.py.new" 2>nul
  pause
  exit /b 1
)

if exist "manual_studio_server.py" (
  copy /y "manual_studio_server.py" "manual_studio_server.py.before-autoupdate.bak" >nul
)
move /y "manual_studio_server.py.new" "manual_studio_server.py" >nul
if errorlevel 1 (
  echo ERROR: No se pudo instalar la actualizacion.
  pause
  exit /b 1
)

echo.
echo Actualizacion aplicada. Se inicia el estudio...
echo La proxima vez podras usar run_manual_studio.bat normalmente.
echo.
python manual_studio_server.py
if errorlevel 1 (
  echo.
  echo El estudio se cerro con un error. Revisa el mensaje anterior.
  pause
)
endlocal
