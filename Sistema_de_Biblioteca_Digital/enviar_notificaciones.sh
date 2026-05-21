#!/bin/bash
# Script para ejecutar notificaciones de vencimiento en Linux/Mac

cd "$(dirname "$0")"

echo ""
echo "================================"
echo "Enviando notificaciones..."
echo "================================"
echo ""

python manage.py enviar_notificaciones_vencimiento

echo ""
echo "Proceso completado."
echo ""
