from django.core.management.base import BaseCommand
from django.utils import timezone
from prestamos.models import Prestamo


class Command(BaseCommand):
    help = 'Envía notificaciones de vencimiento de préstamos próximos a vencer'

    def handle(self, *args, **options):
        prestamos_activos = Prestamo.objects.filter(
            estado__in=['ACTIVO', 'RETRASADO'],
            notificacion_vencimiento_enviada=False
        )

        enviados = 0
        errores = 0

        for prestamo in prestamos_activos:
            if prestamo.enviar_notificacion_vencimiento():
                enviados += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Notificación enviada a {prestamo.usuario.email} - '
                        f'Libro: {prestamo.libro.titulo}'
                    )
                )
            elif prestamo.proxima_a_vencer:
                self.stdout.write(
                    self.style.WARNING(
                        f'! Error enviando notificación a {prestamo.usuario.email} - '
                        f'Libro: {prestamo.libro.titulo}'
                    )
                )
                errores += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Resumen: {enviados} notificaciones enviadas, {errores} errores'
            )
        )
