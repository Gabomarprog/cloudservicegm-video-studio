@echo off
setlocal
cd /d "%~dp0"
title cloudservicegm - Actualizar modalidad 3

echo.
echo ==============================================
echo   Actualizador de cloudservicegm - Modalidad 3
echo ==============================================
echo.
echo Descargando solo los dos archivos de la modalidad 3...
curl.exe --fail --location --silent --show-error --retry 3 --retry-delay 2 ^
  --output "manual_studio_server.py.new" ^
  "https://raw.githubusercontent.com/Gabomarprog/cloudservicegm-video-studio/main/manual_studio_server.py"
if errorlevel 1 goto download_error

if not exist "web" mkdir "web"
curl.exe --fail --location --silent --show-error --retry 3 --retry-delay 2 ^
  --output "web\manual.html.new" ^
  "https://raw.githubusercontent.com/Gabomarprog/cloudservicegm-video-studio/main/web/manual.html"
if errorlevel 1 goto download_error

echo Comprobando los archivos descargados...
python -c "from pathlib import Path; p=Path('manual_studio_server.py.new'); compile(p.read_text(encoding='utf-8'), 'manual_studio_server.py', 'exec'); from html.parser import HTMLParser; h=HTMLParser(); h.feed(Path('web/manual.html.new').read_text(encoding='utf-8')); h.close()"
if errorlevel 1 (
  echo ERROR: La comprobacion fallo. No se reemplazo ningun archivo.
  del /q "manual_studio_server.py.new" 2>nul
  del /q "web\manual.html.new" 2>nul
  pause
  exit /b 1
)

if exist "manual_studio_server.py" (
  copy /y "manual_studio_server.py" "manual_studio_server.py.before-autoupdate.bak" >nul
)
if exist "web\manual.html" (
  copy /y "web\manual.html" "web\manual.html.before-autoupdate.bak" >nul
)

move /y "manual_studio_server.py.new" "manual_studio_server.py" >nul
if errorlevel 1 goto install_error
move /y "web\manual.html.new" "web\manual.html" >nul
if errorlevel 1 goto install_error

echo.
echo Actualizacion aplicada. El catalogo se sincronizara desde GitHub.
echo Se inicia el estudio actualizado...
echo.
python manual_studio_server.py
if errorlevel 1 (
  echo.
  echo El estudio se cerro con un error. Revisa el mensaje anterior.
  pause
)
endlocal
exit /b 0

:download_error
echo.
echo ERROR: No se pudieron descargar los archivos desde GitHub.
del /q "manual_studio_server.py.new" 2>nul
del /q "web\manual.html.new" 2>nul
pause
exit /b 1

:install_error
echo.
echo ERROR: No se pudo instalar uno de los archivos. Hay copias de respaldo .bak.
pause
exit /b 1
