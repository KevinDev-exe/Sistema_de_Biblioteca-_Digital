from django.core.management.base import BaseCommand
from django.utils import timezone
from prestamos.models import Prestamo
from notificaciones.services import ServicioNotificaciones


class Command(BaseCommand):
    help = 'Envía notificaciones de vencimiento y procesa notificaciones pendientes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reintentos',
            action='store_true',
            help='Reintenta enviar notificaciones que fallaron'
        )

        parser.add_argument(
            '--pendientes',
            action='store_true',
            help='Envía todas las notificaciones pendientes'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔔 Iniciando notificaciones...\n'))

        reintentos = options.get('reintentos')
        pendientes = options.get('pendientes')

        if pendientes:
            self.procesar_pendientes()

        if reintentos:
            self.procesar_reintentos()

        if not reintentos and not pendientes:
            self.procesar_vencimientos()

        self.stdout.write(self.style.SUCCESS('\n✅ Proceso completado.'))

    def procesar_vencimientos(self):
        """Procesa vencimientos próximos"""
        self.stdout.write('📋 Buscando préstamos próximos a vencer...\n')

        prestamos_activos = Prestamo.objects.filter(
            estado__in=['ACTIVO', 'RETRASADO']
        )

        enviadas = 0
        for prestamo in prestamos_activos:
            if prestamo.proxima_a_vencer:
                if ServicioNotificaciones.notificar_vencimiento_proximo(prestamo):
                    enviadas += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Notificación de vencimiento: {prestamo.usuario.email} '
                            f'({prestamo.libro.titulo})'
                        )
                    )

        self.stdout.write(self.style.SUCCESS(f'\n📊 {enviadas} notificaciones de vencimiento enviadas'))

    def procesar_pendientes(self):
        """Procesa notificaciones pendientes"""
        self.stdout.write('📋 Procesando notificaciones pendientes...\n')

        resultado = ServicioNotificaciones.enviar_notificaciones_pendientes()

        self.stdout.write(
            self.style.SUCCESS(
                f'✓ {resultado["enviadas"]} notificaciones enviadas\n'
                f'✗ {resultado["errores"]} errores'
            )
        )

    def procesar_reintentos(self):
        """Reintenta notificaciones fallidas"""
        self.stdout.write('🔄 Reintentando notificaciones fallidas...\n')

        reintentadas = ServicioNotificaciones.reintentar_notificaciones_fallidas()

        self.stdout.write(
            self.style.SUCCESS(f'✓ {reintentadas} notificaciones reintentadas')
        )
