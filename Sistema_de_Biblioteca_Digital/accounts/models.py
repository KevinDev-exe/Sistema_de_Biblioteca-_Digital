from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):

    ROLES = (
        ('ADMIN', 'Administrador/Bibliotecario'),
        ('LECTOR', 'Lector'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, blank=True)

    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True)

    rol = models.CharField(max_length=20, choices=ROLES, default='LECTOR')

    sancionado = models.BooleanField(default=False)

    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username