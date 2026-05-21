from django.contrib import admin

from .models import Prestamo


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "libro", "fecha_prestamo", "fecha_devolucion", "fecha_entrega", "estado", "multa")
    list_filter = ("estado", "fecha_prestamo", "fecha_devolucion")
    search_fields = ("usuario__username", "usuario__email", "libro__titulo", "libro__isbn")
    autocomplete_fields = ("usuario", "libro")
    ordering = ("-fecha_prestamo",)

