from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Reserva(models.Model):
    class Estados(models.TextChoices):
        ACTIVA = "activa", "Activa"
        ATENDIDA = "atendida", "Atendida"
        CANCELADA = "cancelada", "Cancelada"
        EXPIRADA = "expirada", "Expirada"

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reservas")
    libro = models.ForeignKey("libros.Libro", on_delete=models.PROTECT, related_name="reservas")
    fecha_reserva = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=Estados.choices, default=Estados.ACTIVA)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha_reserva"]
        verbose_name = "reserva"
        verbose_name_plural = "reservas"
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "libro"],
                condition=models.Q(estado="activa"),
                name="reserva_activa_unica_por_usuario_libro",
            )
        ]

    def __str__(self):
        return f"{self.libro} reservado por {self.usuario}"

    def clean(self):
        if self.estado == self.Estados.ACTIVA and self.libro_id:
            qs = Reserva.objects.filter(usuario=self.usuario, libro=self.libro, estado=self.Estados.ACTIVA)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("El usuario ya tiene una reserva activa para este libro.")
            prestamos_activos = self.libro.prestamos.filter(estado__in=["ACTIVO", "RETRASADO"]).count()
            reservas_activas = self.libro.reservas.filter(estado=self.Estados.ACTIVA)
            if self.pk:
                reservas_activas = reservas_activas.exclude(pk=self.pk)
            if prestamos_activos + reservas_activas.count() >= self.libro.cantidad:
                raise ValidationError("No hay stock disponible para reservar este libro.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if hasattr(self.libro, 'sincronizar_estado'):
            self.libro.sincronizar_estado()

    def delete(self, *args, **kwargs):
        libro = self.libro
        super().delete(*args, **kwargs)
        if hasattr(libro, 'sincronizar_estado'):
            libro.sincronizar_estado()

