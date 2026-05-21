from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Notificacion
from prestamos.models import Prestamo
import logging

logger = logging.getLogger(__name__)


class ServicioNotificaciones:
    """Servicio centralizado para gestionar notificaciones"""

    @staticmethod
    def crear_notificacion(prestamo, tipo, asunto, mensaje, usuario=None):
        """Crea una notificación en BD"""
        notif = Notificacion.objects.create(
            prestamo=prestamo,
            usuario=usuario or prestamo.usuario,
            tipo=tipo,
            asunto=asunto,
            mensaje=mensaje
        )
        return notif

    @staticmethod
    def enviar_notificacion(notificacion):
        """Envía una notificación por email"""
        try:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body style="margin: 0; padding: 0; background-color: #f3f4f6;">
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 20px auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                    <div style="background-color: #0d6efd; color: white; padding: 24px; text-align: center;">
                        <h2 style="margin: 0; font-size: 24px; font-weight: 700;">Biblioteca Digital</h2>
                    </div>
                    <div style="padding: 32px; background-color: #ffffff; color: #334155;">
                        <h3 style="margin-top: 0; color: #111827; font-size: 20px;">{notificacion.asunto}</h3>
                        <p style="white-space: pre-line; line-height: 1.7; font-size: 16px;">{notificacion.mensaje}</p>
                    </div>
                    <div style="background-color: #f8fafc; padding: 20px; text-align: center; color: #64748b; font-size: 13px; border-top: 1px solid #e2e8f0;">
                        <p style="margin: 0;">Este es un mensaje automático del Sistema de Biblioteca Digital.</p>
                        <p style="margin: 5px 0 0 0;">Por favor no respondas a este correo.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            send_mail(
                notificacion.asunto,
                notificacion.mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [notificacion.usuario.email],
                fail_silently=False,
                html_message=html_content
            )
            notificacion.marcar_enviada()
            logger.info(
                f'Notificación enviada a {notificacion.usuario.email} - '
                f'Tipo: {notificacion.get_tipo_display()}'
            )
            return True

        except Exception as e:
            notificacion.marcar_fallida(str(e))
            logger.error(
                f'Error enviando notificación {notificacion.id}: {str(e)}'
            )
            return False

    @staticmethod
    def notificar_aprobacion_prestamo(prestamo):
        """Notifica al usuario que su solicitud fue aprobada"""
        asunto = 'Tu solicitud de préstamo ha sido aprobada'
        mensaje = (
            f'Hola {prestamo.usuario.first_name or prestamo.usuario.username},\n\n'
            f'Tu solicitud de préstamo para el libro "{prestamo.libro.titulo}" '
            f'ha sido aprobada.\n\n'
            f'Fecha de devolución: {prestamo.fecha_devolucion}\n'
            f'Por favor, devuelve el libro antes de esta fecha.\n\n'
            f'Saludos,\nBiblioteca Digital'
        )

        notif = ServicioNotificaciones.crear_notificacion(
            prestamo=prestamo,
            tipo='APROBACION',
            asunto=asunto,
            mensaje=mensaje
        )

        return ServicioNotificaciones.enviar_notificacion(notif)

    @staticmethod
    def notificar_vencimiento_proximo(prestamo):
        """Notifica cuando faltan 0-2 días para vencer"""
        if not prestamo.proxima_a_vencer:
            return False

        # Evitar duplicados
        notif_existente = Notificacion.objects.filter(
            prestamo=prestamo,
            tipo='VENCIMIENTO',
            estado='ENVIADA'
        ).exists()

        if notif_existente:
            return False

        dias = prestamo.dias_para_vencimiento
        asunto = f'Recordatorio: Devolución de "{prestamo.libro.titulo}" próxima a vencer'
        mensaje = (
            f'Hola {prestamo.usuario.first_name or prestamo.usuario.username},\n\n'
            f'Te recordamos que tu préstamo del libro "{prestamo.libro.titulo}" '
            f'debe ser devuelto en {dias} día{"s" if dias != 1 else ""}.\n\n'
            f'Fecha de devolución: {prestamo.fecha_devolucion}\n'
            f'Por favor, devuelve el libro antes de esta fecha para evitar multas.\n\n'
            f'Saludos,\nBiblioteca Digital'
        )

        notif = ServicioNotificaciones.crear_notificacion(
            prestamo=prestamo,
            tipo='VENCIMIENTO',
            asunto=asunto,
            mensaje=mensaje
        )

        return ServicioNotificaciones.enviar_notificacion(notif)

    @staticmethod
    def notificar_devolucion(prestamo):
        """Notifica la confirmación de devolución"""
        asunto = 'Devolución de libro registrada'
        multa_info = f'\nMulta por retraso: ${prestamo.multa}' if prestamo.multa > 0 else ''
        mensaje = (
            f'Hola {prestamo.usuario.first_name or prestamo.usuario.username},\n\n'
            f'Tu devolución del libro "{prestamo.libro.titulo}" ha sido registrada.\n\n'
            f'Fecha de entrega: {prestamo.fecha_entrega}{multa_info}\n\n'
            f'Saludos,\nBiblioteca Digital'
        )

        notif = ServicioNotificaciones.crear_notificacion(
            prestamo=prestamo,
            tipo='DEVOLUCION',
            asunto=asunto,
            mensaje=mensaje
        )

        return ServicioNotificaciones.enviar_notificacion(notif)

    @staticmethod
    def notificar_retraso(prestamo):
        """Notifica sobre préstamo retrasado"""
        if prestamo.estado != 'RETRASADO':
            return False

        # Evitar duplicados
        notif_existente = Notificacion.objects.filter(
            prestamo=prestamo,
            tipo='RETRASO',
            estado='ENVIADA'
        ).exists()

        if notif_existente:
            return False

        dias = prestamo.dias_retraso
        asunto = f'Alerta: Tu préstamo de "{prestamo.libro.titulo}" está retrasado'
        mensaje = (
            f'Hola {prestamo.usuario.first_name or prestamo.usuario.username},\n\n'
            f'Tu préstamo del libro "{prestamo.libro.titulo}" está retrasado '
            f'por {dias} día{"s" if dias != 1 else ""}.\n\n'
            f'Multa acumulada: ${prestamo.multa}\n\n'
            f'Por favor, devuelve el libro lo antes posible.\n\n'
            f'Saludos,\nBiblioteca Digital'
        )

        notif = ServicioNotificaciones.crear_notificacion(
            prestamo=prestamo,
            tipo='RETRASO',
            asunto=asunto,
            mensaje=mensaje
        )

        return ServicioNotificaciones.enviar_notificacion(notif)

    @staticmethod
    def enviar_notificaciones_pendientes():
        """Envía todas las notificaciones pendientes"""
        notificaciones = Notificacion.objects.filter(
            estado='PENDIENTE'
        )

        enviadas = 0
        errores = 0

        for notif in notificaciones:
            if ServicioNotificaciones.enviar_notificacion(notif):
                enviadas += 1
            else:
                errores += 1

        return {
            'enviadas': enviadas,
            'errores': errores,
            'total': notificaciones.count()
        }

    @staticmethod
    def reintentar_notificaciones_fallidas():
        """Reintenta enviar notificaciones que fallaron"""
        notificaciones = Notificacion.objects.filter(
            estado='FALLIDA',
            intentos__lt=3
        )

        reintentadas = 0
        for notif in notificaciones:
            if ServicioNotificaciones.enviar_notificacion(notif):
                reintentadas += 1

        return reintentadas
