@echo off
REM Script para ejecutar notificaciones de vencimiento en Windows

cd /d "%~dp0"

echo.
echo ================================
echo Enviando notificaciones...
echo ================================
echo.

python manage.py enviar_notificaciones_vencimiento

echo.
echo Proceso completado.
echo.
pause
