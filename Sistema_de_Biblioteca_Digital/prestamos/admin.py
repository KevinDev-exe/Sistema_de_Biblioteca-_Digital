from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Prestamo

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('libro', 'usuario', 'fecha_prestamo', 'fecha_devolucion', 'estado', 'multa')
    list_filter = ('estado',)
    search_fields = ('usuario__username', 'libro__titulo')
    readonly_fields = ('multa', 'creado')