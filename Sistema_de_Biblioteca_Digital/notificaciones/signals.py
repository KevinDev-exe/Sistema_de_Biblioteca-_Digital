from django.db.models.signals import post_save
from django.dispatch import receiver
from prestamos.models import Prestamo
from .services import ServicioNotificaciones
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Prestamo)
def notificar_cambios_prestamo(sender, instance, created, **kwargs):
    """
    Signal que se dispara cuando un Prestamo es creado o actualizado.
    Envía notificaciones según el estado del préstamo.
    """
    try:
        # Si el préstamo acaba de cambiar a ACTIVO (fue aprobado)
        if instance.estado == 'ACTIVO' and not created:
            # Verificar si ya existe una notificación de aprobación enviada
            from .models import Notificacion
            notif_existente = Notificacion.objects.filter(
                prestamo=instance,
                tipo='APROBACION',
                estado='ENVIADA'
            ).exists()

            if not notif_existente:
                ServicioNotificaciones.notificar_aprobacion_prestamo(instance)

        # Si el préstamo cambió a RETRASADO
        if instance.estado == 'RETRASADO':
            ServicioNotificaciones.notificar_retraso(instance)

    except Exception as e:
        logger.error(f'Error en signal de notificación: {str(e)}')
