from celery import shared_task
from django.utils import timezone
from .models import Prestamo
import logging

logger = logging.getLogger(__name__)


@shared_task
def enviar_notificaciones_vencimiento_task():
    """
    Tarea Celery para enviar notificaciones de vencimiento de préstamos.
    Se ejecuta según la programación en celery beat.
    """
    prestamos_activos = Prestamo.objects.filter(
        estado__in=['ACTIVO', 'RETRASADO'],
        notificacion_vencimiento_enviada=False
    )

    enviados = 0
    errores = 0

    for prestamo in prestamos_activos:
        try:
            if prestamo.enviar_notificacion_vencimiento():
                enviados += 1
                logger.info(
                    f'Notificación enviada a {prestamo.usuario.email} - '
                    f'Libro: {prestamo.libro.titulo}'
                )
            elif prestamo.proxima_a_vencer:
                errores += 1
                logger.warning(
                    f'Error enviando notificación a {prestamo.usuario.email}'
                )
        except Exception as e:
            errores += 1
            logger.error(
                f'Excepción en notificación para prestamo {prestamo.id}: {str(e)}'
            )

    logger.info(f'Resumen: {enviados} enviadas, {errores} errores')
    return {
        'enviados': enviados,
        'errores': errores,
        'timestamp': timezone.now().isoformat()
    }
