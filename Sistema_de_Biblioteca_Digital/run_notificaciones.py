#!/usr/bin/env python
"""
Script para enviar notificaciones de vencimiento de préstamos.
Puede ejecutarse manualmente o programarse con cron/Task Scheduler.
"""

import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sistema_de_Biblioteca_Digital.settings')
django.setup()

from django.core.management import call_command

if __name__ == '__main__':
    print('🔔 Iniciando envío de notificaciones de vencimiento...')
    call_command('enviar_notificaciones_vencimiento')
    print('✅ Proceso completado.')
