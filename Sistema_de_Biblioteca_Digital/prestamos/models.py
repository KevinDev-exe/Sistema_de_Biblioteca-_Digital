from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from libros.models import Libro
from django.utils import timezone
from decimal import Decimal


class Prestamo(models.Model):

    ESTADOS = [
        ('ACTIVO', 'Activo'),
        ('DEVUELTO', 'Devuelto'),
        ('RETRASADO', 'Retrasado'),
        ('CANCELADO', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='prestamos')
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT, related_name='prestamos')
    fecha_prestamo = models.DateField(default=timezone.localdate)
    fecha_devolucion = models.DateField()
    fecha_entrega = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ACTIVO')
    multa = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    observaciones = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_prestamo']
        verbose_name = 'préstamo'
        verbose_name_plural = 'préstamos'

    def __str__(self):
        return f'{self.libro} - {self.usuario.username}'

    @property
    def dias_retraso(self):
        referencia = self.fecha_entrega or timezone.localdate()
        if referencia <= self.fecha_devolucion:
            return 0
        return (referencia - self.fecha_devolucion).days

    def calcular_multa(self):
        return Decimal(self.dias_retraso * 1000).quantize(Decimal('0.01'))

    def marcar_devuelto(self):
        self.fecha_entrega = timezone.localdate()
        self.estado = 'DEVUELTO'
        self.multa = self.calcular_multa()
        self.save()

    def save(self, *args, **kwargs):
        if self.estado == 'ACTIVO' and self.fecha_devolucion < timezone.localdate():
            self.estado = 'RETRASADO'
        if self.estado in ['DEVUELTO', 'RETRASADO']:
            self.multa = self.calcular_multa()
        super().save(*args, **kwargs)
        activos = self.libro.prestamos.filter(estado__in=['ACTIVO', 'RETRASADO']).count()
        self.libro.disponibles = max(0, self.libro.cantidad - activos)
        self.libro.estado = 'PRESTADO' if self.libro.disponibles == 0 else 'DISPONIBLE'
        self.libro.save()