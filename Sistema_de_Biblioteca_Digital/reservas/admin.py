from django.contrib import admin

from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "libro", "fecha_reserva", "estado")
    list_filter = ("estado", "fecha_reserva")
    search_fields = ("usuario__username", "usuario__email", "libro__titulo", "libro__isbn")
    # autocomplete_fields = ("usuario", "libro")
    ordering = ("-fecha_reserva",)

