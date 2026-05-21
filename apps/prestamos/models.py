from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Prestamo(models.Model):
    class Estados(models.TextChoices):
        ACTIVO = "activo", "Activo"
        DEVUELTO = "devuelto", "Devuelto"
        RETRASADO = "retrasado", "Retrasado"
        CANCELADO = "cancelado", "Cancelado"

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="prestamos")
    libro = models.ForeignKey("libros.Libro", on_delete=models.PROTECT, related_name="prestamos")
    fecha_prestamo = models.DateField(default=timezone.localdate)
    fecha_devolucion = models.DateField()
    fecha_entrega = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=Estados.choices, default=Estados.ACTIVO)
    multa = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    observaciones = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_prestamo"]
        verbose_name = "prestamo"
        verbose_name_plural = "prestamos"
        indexes = [
            models.Index(fields=["estado"]),
            models.Index(fields=["fecha_prestamo"]),
            models.Index(fields=["fecha_devolucion"]),
        ]

    def __str__(self):
        return f"{self.libro} - {self.usuario}"

    def clean(self):
        if self.fecha_devolucion and self.fecha_prestamo and self.fecha_devolucion < self.fecha_prestamo:
            raise ValidationError({"fecha_devolucion": "La fecha de devolucion no puede ser anterior al prestamo."})
        if self.fecha_entrega and self.fecha_entrega < self.fecha_prestamo:
            raise ValidationError({"fecha_entrega": "La fecha de entrega no puede ser anterior al prestamo."})
        if self.estado in [self.Estados.ACTIVO, self.Estados.RETRASADO] and self.libro_id:
            qs = Prestamo.objects.filter(libro=self.libro, estado__in=[self.Estados.ACTIVO, self.Estados.RETRASADO])
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            reservas_activas = self.libro.reservas.filter(estado="activa").count() if self.libro_id else 0
            if qs.count() + reservas_activas >= self.libro.cantidad:
                raise ValidationError("No hay stock disponible para prestar este libro.")

    @property
    def dias_retraso(self):
        referencia = self.fecha_entrega or timezone.localdate()
        if referencia <= self.fecha_devolucion:
            return 0
        return (referencia - self.fecha_devolucion).days

    def calcular_multa(self):
        return Decimal(self.dias_retraso * 1000).quantize(Decimal("0.01"))

    def marcar_devuelto(self):
        self.fecha_entrega = timezone.localdate()
        self.estado = self.Estados.DEVUELTO
        self.multa = self.calcular_multa()
        self.save()

    def save(self, *args, **kwargs):
        if self.estado == self.Estados.ACTIVO and self.fecha_devolucion < timezone.localdate():
            self.estado = self.Estados.RETRASADO
        if self.estado in [self.Estados.DEVUELTO, self.Estados.RETRASADO]:
            self.multa = self.calcular_multa()
        super().save(*args, **kwargs)
        self.libro.sincronizar_estado()

    def delete(self, *args, **kwargs):
        libro = self.libro
        super().delete(*args, **kwargs)
        libro.sincronizar_estado()

