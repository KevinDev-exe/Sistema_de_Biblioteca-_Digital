from django.db import models


class Autor(models.Model):

    nombre = models.CharField(
        max_length=200
    )

    def __str__(self):

        return self.nombre


class Categoria(models.Model):

    nombre = models.CharField(
        max_length=200
    )

    def __str__(self):

        return self.nombre


class Libro(models.Model):

    ESTADOS = [

        ('DISPONIBLE', 'Disponible'),

        ('PRESTADO', 'Prestado'),

        ('RESERVADO', 'Reservado'),

        ('RETRASADO', 'Retrasado'),

    ]

    titulo = models.CharField(
        max_length=200
    )

    isbn = models.CharField(
        max_length=20,
        unique=True
    )

    descripcion = models.TextField()

    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    imagen = models.ImageField(
        upload_to='libros/',
        blank=True,
        null=True
    )

    cantidad = models.PositiveIntegerField(
        default=1
    )

    disponibles = models.PositiveIntegerField(
        default=1
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='DISPONIBLE'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )
    

    def __str__(self):

        return self.titulo
    
   