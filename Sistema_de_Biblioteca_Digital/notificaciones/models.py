from django.db import models
from django.contrib.auth.models import User
from prestamos.models import Prestamo
from django.utils import timezone


class Notificacion(models.Model):

    TIPOS = [
        ('APROBACION', 'Aprobación de Préstamo'),
        ('VENCIMIENTO', 'Recordatorio de Vencimiento'),
        ('DEVOLUCION', 'Confirmación de Devolución'),
        ('RETRASO', 'Notificación de Retraso'),
    ]

    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('ENVIADA', 'Enviada'),
        ('FALLIDA', 'Fallida'),
        ('CANCELADA', 'Cancelada'),
    ]

    prestamo = models.ForeignKey(
        Prestamo,
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notificaciones_recibidas'
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS,
        default='VENCIMIENTO'
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='PENDIENTE'
    )

    asunto = models.CharField(
        max_length=200
    )

    mensaje = models.TextField()

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_envio = models.DateTimeField(
        blank=True,
        null=True
    )

    intentos = models.IntegerField(
        default=0
    )

    error = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'notificación'
        verbose_name_plural = 'notificaciones'
        indexes = [
            models.Index(fields=['estado', 'tipo']),
            models.Index(fields=['usuario', 'fecha_creacion']),
        ]

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.usuario.username}'

    @property
    def puede_reintentarse(self):
        return self.estado == 'FALLIDA' and self.intentos < 3

    def marcar_enviada(self):
        self.estado = 'ENVIADA'
        self.fecha_envio = timezone.now()
        self.save()

    def marcar_fallida(self, error_msg=''):
        self.estado = 'FALLIDA'
        self.intentos += 1
        if error_msg:
            self.error = error_msg
        self.save()
