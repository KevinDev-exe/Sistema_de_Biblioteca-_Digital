from django.contrib import admin
from .models import Notificacion


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'get_libro',
        'usuario',
        'get_tipo_display',
        'get_estado_display',
        'fecha_creacion',
        'intentos'
    ]

    list_filter = ['tipo', 'estado', 'fecha_creacion']

    search_fields = ['usuario__username', 'prestamo__libro__titulo', 'asunto']

    readonly_fields = [
        'prestamo',
        'usuario',
        'fecha_creacion',
        'fecha_envio',
        'intentos',
        'error'
    ]

    fieldsets = (
        ('Información General', {
            'fields': ('prestamo', 'usuario', 'tipo', 'estado')
        }),
        ('Contenido', {
            'fields': ('asunto', 'mensaje')
        }),
        ('Historial de Envío', {
            'fields': ('fecha_creacion', 'fecha_envio', 'intentos', 'error')
        }),
    )

    def get_libro(self, obj):
        return obj.prestamo.libro.titulo if obj.prestamo else '-'
    get_libro.short_description = 'Libro'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
