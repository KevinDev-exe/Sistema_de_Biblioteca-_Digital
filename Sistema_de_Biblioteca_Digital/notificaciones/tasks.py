from celery import shared_task
from django.utils import timezone
from .services import ServicioNotificaciones
from prestamos.models import Prestamo
import logging

logger = logging.getLogger(__name__)


@shared_task
def enviar_notificaciones_vencimiento():
    """Tarea Celery para enviar notificaciones de vencimiento"""
    try:
        prestamos = Prestamo.objects.filter(
            estado__in=['ACTIVO', 'RETRASADO']
        )

        enviadas = 0
        for prestamo in prestamos:
            if prestamo.proxima_a_vencer:
                if ServicioNotificaciones.notificar_vencimiento_proximo(prestamo):
                    enviadas += 1

        logger.info(f'{enviadas} notificaciones de vencimiento enviadas')
        return {'enviadas': enviadas}

    except Exception as e:
        logger.error(f'Error en tarea de vencimiento: {str(e)}')
        return {'error': str(e)}


@shared_task
def procesar_notificaciones_pendientes():
    """Tarea Celery para procesar notificaciones pendientes"""
    try:
        resultado = ServicioNotificaciones.enviar_notificaciones_pendientes()
        logger.info(f'Notificaciones procesadas: {resultado}')
        return resultado

    except Exception as e:
        logger.error(f'Error procesando notificaciones: {str(e)}')
        return {'error': str(e)}


@shared_task
def reintentar_notificaciones_fallidas():
    """Tarea Celery para reintentar notificaciones fallidas"""
    try:
        reintentadas = ServicioNotificaciones.reintentar_notificaciones_fallidas()
        logger.info(f'{reintentadas} notificaciones reintentadas')
        return {'reintentadas': reintentadas}

    except Exception as e:
        logger.error(f'Error reintentando notificaciones: {str(e)}')
        return {'error': str(e)}
