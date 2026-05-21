from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.libros.models import Autor, Categoria, Libro
from apps.prestamos.models import Prestamo
from apps.reservas.models import Reserva
from apps.usuarios.models import Usuario


class Command(BaseCommand):
    help = "Carga datos iniciales para presentar la Biblioteca Digital."

    def handle(self, *args, **options):
        admin, _ = Usuario.objects.get_or_create(
            username="bibliotecario",
            defaults={
                "email": "bibliotecario@demo.com",
                "nombre": "Bibliotecario Principal",
                "rol": Usuario.Roles.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin.set_password("Admin12345")
        admin.save()

        lector, _ = Usuario.objects.get_or_create(
            username="lector",
            defaults={"email": "lector@demo.com", "nombre": "Lector Demo", "rol": Usuario.Roles.LECTOR},
        )
        lector.set_password("Lector12345")
        lector.save()

        categorias = {
            nombre: Categoria.objects.get_or_create(nombre=nombre, defaults={"descripcion": descripcion})[0]
            for nombre, descripcion in {
                "Ingenieria": "Libros tecnicos y de desarrollo de software.",
                "Literatura": "Novelas, poesia y narrativa.",
                "Ciencias": "Textos de ciencia, investigacion y divulgacion.",
                "Gestion": "Administracion, liderazgo y proyectos.",
            }.items()
        }
        autores = {
            nombre: Autor.objects.get_or_create(nombre=nombre, defaults={"nacionalidad": nacionalidad})[0]
            for nombre, nacionalidad in {
                "Robert C. Martin": "Estados Unidos",
                "Gabriel Garcia Marquez": "Colombia",
                "Jane Austen": "Reino Unido",
                "Stephen Hawking": "Reino Unido",
            }.items()
        }

        libros = [
            ("Codigo Limpio", "9780132350884", autores["Robert C. Martin"], categorias["Ingenieria"], 4),
            ("Cien anos de soledad", "9780307474728", autores["Gabriel Garcia Marquez"], categorias["Literatura"], 3),
            ("Orgullo y prejuicio", "9780141439518", autores["Jane Austen"], categorias["Literatura"], 2),
            ("Historia del tiempo", "9780553380163", autores["Stephen Hawking"], categorias["Ciencias"], 2),
        ]
        creados = []
        for titulo, isbn, autor, categoria, cantidad in libros:
            libro, _ = Libro.objects.get_or_create(
                isbn=isbn,
                defaults={
                    "titulo": titulo,
                    "descripcion": f"Ejemplar de {titulo} disponible en la biblioteca digital.",
                    "autor": autor,
                    "categoria": categoria,
                    "cantidad": cantidad,
                },
            )
            creados.append(libro)

        Prestamo.objects.get_or_create(
            usuario=lector,
            libro=creados[0],
            estado=Prestamo.Estados.ACTIVO,
            defaults={
                "fecha_prestamo": timezone.localdate() - timedelta(days=2),
                "fecha_devolucion": timezone.localdate() + timedelta(days=5),
            },
        )
        Reserva.objects.get_or_create(usuario=lector, libro=creados[1], estado=Reserva.Estados.ACTIVA)

        self.stdout.write(self.style.SUCCESS("Datos iniciales cargados."))
        self.stdout.write("Admin: bibliotecario / Admin12345")
        self.stdout.write("Lector: lector / Lector12345")

