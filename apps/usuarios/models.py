from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Administrador/Bibliotecario"
        LECTOR = "lector", "Lector"

    nombre = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=Roles.choices, default=Roles.LECTOR)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    sancionado = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["email", "nombre"]

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ["-fecha_registro"]

    def __str__(self):
        return self.get_full_name() or self.nombre or self.username

    @property
    def es_bibliotecario(self):
        return self.is_staff or self.rol == self.Roles.ADMIN

