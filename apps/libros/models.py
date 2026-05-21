from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count, Q
from django.urls import reverse


class TimeStampedModel(models.Model):
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Autor(TimeStampedModel):
    nombre = models.CharField(max_length=180, unique=True)
    nacionalidad = models.CharField(max_length=120, blank=True)
    biografia = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "autor"
        verbose_name_plural = "autores"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("libros:autor_list")


class Categoria(TimeStampedModel):
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("libros:categoria_list")


class Libro(TimeStampedModel):
    class Estados(models.TextChoices):
        DISPONIBLE = "disponible", "Disponible"
        PRESTADO = "prestado", "Prestado"
        RESERVADO = "reservado", "Reservado"
        RETRASADO = "retrasado", "Retrasado"

    titulo = models.CharField(max_length=220)
    isbn = models.CharField("ISBN", max_length=20, unique=True)
    descripcion = models.TextField(blank=True)
    portada = models.ImageField(upload_to="portadas/", blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=20, choices=Estados.choices, default=Estados.DISPONIBLE)
    fecha_publicacion = models.DateField(blank=True, null=True)
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT, related_name="libros")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="libros")

    class Meta:
        ordering = ["titulo"]
        verbose_name = "libro"
        verbose_name_plural = "libros"
        indexes = [
            models.Index(fields=["titulo"]),
            models.Index(fields=["isbn"]),
            models.Index(fields=["estado"]),
        ]

    def __str__(self):
        return self.titulo

    def clean(self):
        if self.cantidad < 1:
            raise ValidationError({"cantidad": "La cantidad debe ser mayor o igual a 1."})

    def get_absolute_url(self):
        return reverse("libros:libro_detail", kwargs={"pk": self.pk})

    @property
    def prestamos_activos(self):
        return self.prestamos.filter(estado__in=["activo", "retrasado"]).count()

    @property
    def reservas_activas(self):
        return self.reservas.filter(estado="activa").count()

    @property
    def cantidad_disponible(self):
        return max(self.cantidad - self.prestamos_activos - self.reservas_activas, 0)

    def hay_stock(self):
        return self.cantidad_disponible > 0

    def sincronizar_estado(self, guardar=True):
        nuevo_estado = self.Estados.DISPONIBLE
        if self.prestamos.filter(estado="retrasado").exists():
            nuevo_estado = self.Estados.RETRASADO
        elif self.reservas.filter(estado="activa").count() >= self.cantidad:
            nuevo_estado = self.Estados.RESERVADO
        elif self.prestamos.filter(estado="activo").count() >= self.cantidad:
            nuevo_estado = self.Estados.PRESTADO
        if self.estado != nuevo_estado:
            self.estado = nuevo_estado
            if guardar:
                self.save(update_fields=["estado", "actualizado"])
        return nuevo_estado

    @classmethod
    def mas_reservados(cls, limite=8):
        return (
            cls.objects.filter(activo=True)
            .annotate(total_reservas=Count("reservas", filter=Q(reservas__estado__in=["activa", "atendida"])))
            .order_by("-total_reservas", "titulo")[:limite]
        )

